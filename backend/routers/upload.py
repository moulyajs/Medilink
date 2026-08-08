import os
import uuid
from typing import List, Optional
from datetime import date as Date

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
import traceback
from database import get_db
from utils.dependencies import get_current_patient

from models.patient import Patient
from models.notification import Notification

from schemas.report_schemas import (
    ReportSummary,
    ReportDetail,
    LabValueResponse,
)

from scripts.app import (
    process_document,
    save_confirmed_report,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ======================================================
# STEP 1 : Upload (Extract only)
# ======================================================

@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient),
):
    try:

        extension = os.path.splitext(file.filename)[1]

        temp_filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            UPLOAD_DIR,
            temp_filename,
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = process_document(
            file_path=file_path,
            patient_id=str(current_patient.patient_id),
        )

        return {
            "temp_file_id": temp_filename,
            "lab_values": result["lab_values"],
            "clinical_notes": result.get(
                "clinical_notes",
                [],
            ),
            "is_duplicate": result.get(
                "is_duplicate",
                False,
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ======================================================
# Models
# ======================================================

class LabValueInput(BaseModel):
    test_name: str
    value: float
    unit: Optional[str] = None
    reference_range: Optional[list[float]] = None
    abnormal: Optional[bool] = None
    date: Optional[Date] = None


class ConfirmUploadRequest(BaseModel):
    temp_file_id: str
    lab_values: List[LabValueInput]


# ======================================================
# STEP 2 : Confirm -> Actually Save
# ======================================================

@router.post("/confirm")
async def confirm_report(
    payload: ConfirmUploadRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):

    file_path = os.path.join(
        UPLOAD_DIR,
        payload.temp_file_id,
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Temporary file expired.",
        )

    try:

        confirmed_labs = [
            lab.dict()
            for lab in payload.lab_values
        ]

        result = save_confirmed_report(
            patient_id=str(current_patient.patient_id),
            file_path=file_path,
            confirmed_lab_values=confirmed_labs,
        )

        os.remove(file_path)

        if result.get("is_duplicate"):
            return result

        patient_id = str(current_patient.patient_id)

        # ==================================================
        # REPORT UPLOADED NOTIFICATION
        # ==================================================

        db.add(
            Notification(
                patient_id=current_patient.patient_id,
                title="Report Uploaded",
                message="Your medical report has been uploaded successfully.",
                notification_type="report",
            )
        )

        # ==================================================
        # TREND NOTIFICATIONS
        # ==================================================

        trend_rows = db.execute(
            text("""
                SELECT
                    test_name,
                    trend
                FROM lab_trends
                WHERE patient_id = :pid
                AND trend <> 'Stable'
            """),
            {
                "pid": patient_id,
            },
        ).fetchall()

        for row in trend_rows:

            message = f"{row.test_name} is now {row.trend}."

            exists = (
                db.query(Notification)
                .filter(
                    Notification.patient_id == current_patient.patient_id,
                    Notification.notification_type == "trend",
                    Notification.message == message,
                )
                .first()
            )

            if not exists:

                db.add(
                    Notification(
                        patient_id=current_patient.patient_id,
                        title="Trend Changed",
                        message=message,
                        notification_type="trend",
                    )
                )

        # ==================================================
        # ANOMALY NOTIFICATIONS
        # ==================================================

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

            message = (
                f"An unusual change was detected in {row.test_name}."
            )

            exists = (
                db.query(Notification)
                .filter(
                    Notification.patient_id == current_patient.patient_id,
                    Notification.notification_type == "anomaly",
                    Notification.message == message,
                )
                .first()
            )

            if not exists:

                db.add(
                    Notification(
                        patient_id=current_patient.patient_id,
                        title="Anomaly Detected",
                        message=message,
                        notification_type="anomaly",
                    )
                )

        db.commit()

        return {
            "message": "Report saved successfully",
            "document_id": str(result["document_id"]),
        }

    

    except Exception as e:
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

# ======================================================
# REPORT LIST
# ======================================================

@router.get("/list", response_model=list[ReportSummary])
def list_reports(
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient),
):

    rows = db.execute(
        text("""
            SELECT
                d.document_id,
                d.document_type,
                d.upload_date,
                COUNT(lr.result_id) AS lab_count,
                BOOL_OR(lr.abnormal_flag) AS has_abnormal
            FROM documents d
            LEFT JOIN lab_results lr
                ON lr.document_id = d.document_id
            WHERE d.patient_id = :pid
            GROUP BY
                d.document_id,
                d.document_type,
                d.upload_date
            ORDER BY d.upload_date DESC
        """),
        {
            "pid": str(current_patient.patient_id),
        },
    ).fetchall()

    reports = []

    for r in rows:

        status = (
            "Pending"
            if r.lab_count == 0
            else (
                "Abnormal"
                if r.has_abnormal
                else "Normal"
            )
        )

        reports.append(
            ReportSummary(
                document_id=r.document_id,
                document_type=r.document_type,
                upload_date=r.upload_date,
                status=status,
                lab_count=r.lab_count,
            )
        )

    return reports


# ======================================================
# REPORT DETAILS
# ======================================================

@router.get("/{document_id}", response_model=ReportDetail)
def get_report_detail(
    document_id: str,
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient),
):

    doc = db.execute(
        text("""
            SELECT
                document_id,
                document_type,
                upload_date
            FROM documents
            WHERE document_id=:did
            AND patient_id=:pid
        """),
        {
            "did": document_id,
            "pid": str(current_patient.patient_id),
        },
    ).fetchone()

    if doc is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    lab_rows = db.execute(
        text("""
            SELECT
                result_id,
                test_name,
                value,
                unit,
                reference_low,
                reference_high,
                abnormal_flag,
                result_date
            FROM lab_results
            WHERE document_id=:did
            ORDER BY test_name
        """),
        {
            "did": document_id,
        },
    ).fetchall()

    lab_values = [
        LabValueResponse(**row._mapping)
        for row in lab_rows
    ]

    has_abnormal = any(
        x.abnormal_flag
        for x in lab_values
    )

    status = (
        "Pending"
        if not lab_values
        else (
            "Abnormal"
            if has_abnormal
            else "Normal"
        )
    )

    return ReportDetail(
        document_id=doc.document_id,
        document_type=doc.document_type,
        upload_date=doc.upload_date,
        status=status,
        lab_values=lab_values,
    )