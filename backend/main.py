from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.timeline_router import router as timeline_router

from sqlalchemy import text

from storage import client, BUCKET
from database import SessionLocal, DB_URL

import uuid
import io

print("MAIN DB URL =", DB_URL)

app = FastAPI()

app.include_router(timeline_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------
# Upload Document
# ----------------------------------------------------

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:

        file_id = str(uuid.uuid4())
        stored_filename = f"{file_id}_{file.filename}"

        content = await file.read()

        client.put_object(
            BUCKET,
            stored_filename,
            io.BytesIO(content),
            length=len(content),
            content_type=file.content_type,
        )

        db = SessionLocal()

        db.execute(
            text("""
                INSERT INTO documents
                (
                    patient_id,
                    document_type,
                    upload_date,
                    file_path
                )
                VALUES
                (
                    :pid,
                    :dtype,
                    NOW(),
                    :path
                )
            """),
            {
                "pid": "cc82f6e5-1e57-43d3-87c8-f5638bcf0858",
                "dtype": file.content_type,
                "path": stored_filename,
            },
        )

        db.commit()
        db.close()

        return {
            "status": "success",
            "file_name": stored_filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
# List Documents
# ----------------------------------------------------

@app.get("/documents")
def get_documents():

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT
                    document_id,
                    patient_id,
                    document_type,
                    upload_date,
                    file_path
                FROM documents
                ORDER BY upload_date DESC
            """)
        ).fetchall()

        return [
            {
                "document_id": str(r.document_id),
                "patient_id": str(r.patient_id),
                "document_type": r.document_type,
                "upload_date": str(r.upload_date),
                "file_path": r.file_path,
            }
            for r in rows
        ]

    finally:
        db.close()



# ----------------------------------------------------
# View PDF
# ----------------------------------------------------

@app.get("/document/{document_id}")
def view_document(document_id: str):

    db = SessionLocal()

    try:

        row = db.execute(
            text("""
                SELECT file_path
                FROM documents
                WHERE document_id = CAST(:id AS UUID)
            """),
            {"id": document_id},
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found",
            )

        obj = client.get_object(
            BUCKET,
            row.file_path,
        )

        return StreamingResponse(
            obj,
            media_type="application/pdf",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        db.close()


# ----------------------------------------------------
# Direct View By File Path
# ----------------------------------------------------

@app.get("/view/{file_path}")
def view_file(file_path: str):

    try:

        obj = client.get_object(
            BUCKET,
            file_path,
        )

        return StreamingResponse(
            obj,
            media_type="application/pdf",
        )

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )