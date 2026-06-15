from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from storage import client, BUCKET
from database import SessionLocal
from sqlalchemy import text
from scripts.timeline_service import get_timeline
import uuid
import io
from database import DB_URL

print("MAIN DB URL =", DB_URL)

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        stored_filename = f"{file_id}_{file.filename}"

        # Read file
        content = await file.read()
        file_stream = io.BytesIO(content)

        # Upload to MinIO
        client.put_object(
            BUCKET,
            stored_filename,
            file_stream,
            length=len(content),
            content_type=file.content_type
        )

        # Save metadata in DB
        db = SessionLocal()

        db.execute(
            text("""
                INSERT INTO documents
                (patient_id, document_type, upload_date, file_path)
                VALUES (:pid, :dtype, NOW(), :path)
            """),
            {
                "pid": 1,  # temporary patient id
                "dtype": file.content_type,
                "path": stored_filename
            }
        )

        db.commit()
        db.close()

        return {
            "status": "success",
            "file_id": file_id,
            "stored_filename": stored_filename
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/")
def get_documents():

    db = SessionLocal()

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

    db.close()

    return docs


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

@app.get("/timeline/{patient_id}")
def timeline(patient_id: int):
    return get_timeline(patient_id)

@app.get("/document/{record_id}")
def get_document(record_id: int):

    db = SessionLocal()

    result = db.execute(
        text("""
        SELECT
            f.file_name,
            f.file_path

        FROM medical_records mr

        JOIN files f
            ON mr.file_id = f.id

        WHERE mr.id = :rid
        """),
        {"rid": record_id}
    )

    row = result.fetchone()

    db.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "file_name": row.file_name,
        "file_path": row.file_path
    }

@app.get("/document/view/{record_id}")
def view_document(record_id: int):

    db = SessionLocal()

    result = db.execute(
        text("""
        SELECT
            f.file_path

        FROM medical_records mr

        JOIN files f
            ON mr.file_id = f.id

        WHERE mr.id = :rid
        """),
        {"rid": record_id}
    )

    row = result.fetchone()

    db.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    try:
        obj = client.get_object(
            BUCKET,
            row.file_path
        )

        return StreamingResponse(
            obj,
            media_type="application/pdf"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/document/view/{record_id}")
def view_document(record_id: int):

    db = SessionLocal()

    result = db.execute(
        text("""
        SELECT f.file_path
        FROM medical_records mr
        JOIN files f
            ON mr.file_id = f.id
        WHERE mr.id = :rid
        """),
        {"rid": record_id}
    )

    row = result.fetchone()

    db.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    obj = client.get_object(
        BUCKET,
        row.file_path
    )

    return StreamingResponse(
        obj,
        media_type="application/pdf"
    )   
#main.py