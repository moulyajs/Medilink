from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from storage import client, BUCKET
from database import SessionLocal
from sqlalchemy import text
import uuid
import io
import tempfile
from datetime import datetime

from scripts.lab_extraction import extract_lab_results
from scripts.chunking import create_chunks
from scripts.embedding import embed_chunks
from scripts.vector_store import insert_chunks
from sqlalchemy import text
from database import SessionLocal

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    db = SessionLocal()

    try:
        file_id = str(uuid.uuid4())
        stored_filename = f"{file_id}_{file.filename}"

        # =========================
        # 📤 Upload to MinIO
        # =========================
        content = await file.read()
        file_stream = io.BytesIO(content)

        client.put_object(
            BUCKET,
            stored_filename,
            file_stream,
            length=len(content),
            content_type=file.content_type
        )

        # =========================
        # 💾 Save to DB
        # =========================
        patient_id = str(uuid.uuid4())  # TEMP (replace with auth later)

        result = db.execute(
            text("""
                INSERT INTO documents
                (patient_id, document_type, upload_date, file_path)
                VALUES (:pid, :dtype, NOW(), :path)
                RETURNING document_id
            """),
            {
                "pid": patient_id,
                "dtype": file.content_type,
                "path": stored_filename
            }
        )

        document_id = result.fetchone()[0]
        db.commit()

        # =========================
        # 🔥 PROCESS DOCUMENT
        # =========================

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            temp_path = tmp.name

        labs = extract_lab_results(temp_path, source="pdf")

        parsed_data = {
            "lab_results": [
                {
                    "test_name": l["test"],
                    "value": l["value"],
                    "unit": l.get("unit"),
                    "reference_range": l.get("reference_range"),
                }
                for l in labs
            ]
        }

        # =========================
        # 🧩 Chunking
        # =========================
        report_date = datetime.now().date()

        chunks = create_chunks(
            parsed_data,
            patient_id=patient_id,
            document_id=document_id,
            report_date=str(report_date)
        )

        # =========================
        # 🧠 Embedding
        # =========================
        embeddings = embed_chunks(chunks)

        # =========================
        # 📡 Store in Qdrant
        # =========================
        insert_chunks(chunks, embeddings)

        return {
            "status": "success",
            "document_id": document_id,
            "chunks_created": len(chunks)
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@app.get("/documents/")
def get_documents():

    db = SessionLocal()

    try:
        result = db.execute(
            text("""
                SELECT document_id, patient_id, document_type, upload_date, file_path
                FROM documents
                ORDER BY upload_date DESC
            """)
        )

        docs = []

        for row in result:
            docs.append({
                "document_id": row.document_id,
                "patient_id": row.patient_id,
                "document_type": row.document_type,
                "upload_date": str(row.upload_date),
                "file_path": row.file_path
            })

        return docs

    finally:
        db.close()


@app.get("/view/{file_path}")
def view_file(file_path: str):

    try:
        obj = client.get_object(BUCKET, file_path)

        return StreamingResponse(
            obj,
            media_type="application/pdf"
        )

    except Exception:
        raise HTTPException(status_code=404, detail="File not found")
    

@app.get("/trend-analysis/{patient_id}")
def get_trend_analysis(patient_id: str):

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT
                    test_name,
                    latest_value,
                    delta,
                    slope,
                    trend,
                    status,
                    data_points
                FROM lab_trends
                WHERE patient_id = :pid
                ORDER BY test_name
            """),
            {"pid": patient_id}
        )

        trends = []

        for row in result:
            trends.append({
                "test_name": row.test_name,
                "latest_value": row.latest_value,
                "delta": row.delta,
                "slope": row.slope,
                "trend": row.trend,
                "status": row.status,
                "data_points": row.data_points
            })

        return trends

    finally:
        db.close()