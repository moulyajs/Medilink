import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from utils.dependencies import get_current_patient

from models.patient import Patient
from models.notification import Notification

from scripts.app import process_document

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient),
):
    try:

        extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            UPLOAD_DIR,
            filename,
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("🚀 Starting AI pipeline...")

        process_document(
            file_path=file_path,
            patient_id=str(current_patient.patient_id),
        )

        patient_id = str(current_patient.patient_id)

        # ======================================
        # Report Uploaded Notification
        # ======================================

        db.add(
            Notification(
                patient_id=current_patient.patient_id,
                title="Report Uploaded",
                message=f"{file.filename} has been uploaded successfully.",
                notification_type="report",
            )
        )

        # ======================================
        # Trend Notifications
        # ======================================

        trend_rows = db.execute(
            text("""
                SELECT test_name, trend
                FROM lab_trends
                WHERE patient_id = :pid
                AND trend <> 'Stable'
            """),
            {
                "pid": patient_id,
            },
        ).fetchall()

        for row in trend_rows:

            existing = (
                db.query(Notification)
                .filter(
                    Notification.patient_id == current_patient.patient_id,
                    Notification.notification_type == "trend",
                    Notification.message
                    == f"{row.test_name} is now {row.trend}.",
                )
                .first()
            )

            if not existing:

                db.add(
                    Notification(
                        patient_id=current_patient.patient_id,
                        title="Trend Changed",
                        message=f"{row.test_name} is now {row.trend}.",
                        notification_type="trend",
                    )
                )

        # ======================================
        # Anomaly Notifications
        # ======================================

        anomaly_rows = db.execute(
            text("""
                SELECT test_name
                FROM patient_anomalies
                WHERE patient_id = :pid
            """),
            {
                "pid": patient_id,
            },
        ).fetchall()

        for row in anomaly_rows:

            existing = (
                db.query(Notification)
                .filter(
                    Notification.patient_id == current_patient.patient_id,
                    Notification.notification_type == "anomaly",
                    Notification.message
                    == f"An unusual change was detected in {row.test_name}.",
                )
                .first()
            )

            if not existing:

                db.add(
                    Notification(
                        patient_id=current_patient.patient_id,
                        title="Anomaly Detected",
                        message=f"An unusual change was detected in {row.test_name}.",
                        notification_type="anomaly",
                    )
                )

        db.commit()

        print("✅ AI pipeline completed")

        return {
            "message": "File uploaded and processed successfully",
            "patient_id": patient_id,
            "file_path": file_path,
            "filename": filename,
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )