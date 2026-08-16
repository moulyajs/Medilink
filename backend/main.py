from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from sqlalchemy import text

from storage import client, BUCKET
from database import SessionLocal, DB_URL

from fastapi import Depends
from utils.dependencies import get_current_patient
from models.patient import Patient

import uuid
import io

print("MAIN DB URL =", DB_URL)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.patient import Patient
from models.profile import Profile
from models.otp import EmailOTP
from database import Base, engine
from routers.profile import router as profile_router
from routers.auth import router as auth_router
from routers.support import router as support_router
from routers.report_issue import router as report_issue_router
from routers.device import router as device_router
from routers.notification import router as notification_router
from routers.chat import router as chat_router
from routers.upload import router as upload_router
from routers.trend import router as trend_router
from routers import anomaly
from routers.timeline import router as timeline_router
from models.notification import Notification
from models.notification_settings import NotificationSettings
from routers.notification_history import (
    router as notification_history_router,
)
# Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Medilink API",
    description="Backend API for Medilink",
    version="1.0.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to Medilink API 🚀"
    }




# ----------------------------------------------------
# Upload Document
# ----------------------------------------------------

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient)
):
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
                "pid": str(current_patient.patient_id),
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
def get_documents(
    current_patient: Patient = Depends(get_current_patient)
):

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
                WHERE patient_id = :pid
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
def view_document(
    document_id: str,
    current_patient: Patient = Depends(get_current_patient)
):
    db = SessionLocal()

    try:

        row = db.execute(
            text("""
                SELECT file_path
                FROM documents
                WHERE document_id = CAST(:id AS UUID)
                AND patient_id = :pid
            """),
            {
               "id": document_id,
               "pid": str(current_patient.patient_id),
            },
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

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(support_router)
app.include_router(report_issue_router)
app.include_router(device_router)
app.include_router(notification_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(trend_router)
app.include_router(anomaly.router)
app.include_router(notification_history_router)
app.include_router(timeline_router)
