from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from storage import client, BUCKET
from database import SessionLocal
from sqlalchemy import text
import uuid
import io

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

#main.py