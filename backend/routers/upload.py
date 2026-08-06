import os
import uuid
from typing import List, Optional
from datetime import date as Date
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel

from database import get_db
from utils.dependencies import get_current_patient
from models.patient import Patient
from schemas.report_schemas import ReportSummary, ReportDetail, LabValueResponse
from scripts.app import process_document, save_confirmed_report

router = APIRouter(prefix="/reports", tags=["Reports"])

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#print(">>> upload.py loaded <<<")
#print("Current working directory:", os.getcwd())
#print("Upload dir exists:", os.path.exists(UPLOAD_DIR))


# ============================================================
# STEP 1: UPLOAD — extract only, nothing saved yet
# ============================================================

@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient),
):
    try:
        extension = os.path.splitext(file.filename)[1]
        temp_filename = f"{uuid.uuid4()}{extension}"
        file_path = os.path.join(UPLOAD_DIR, temp_filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = process_document(
            file_path=file_path,
            patient_id=str(current_patient.patient_id),
        )

        return {
            "temp_file_id": temp_filename,  # frontend must send this back on confirm
            "lab_values": result["lab_values"],
            "clinical_notes": result.get("clinical_notes", []),
            "is_duplicate": result.get("is_duplicate", False),
        }

    except Exception as e:
        #traceback.print_exc()          # <-- add this
        #print("ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


class LabValueInput(BaseModel):
    test_name: str
    value: float
    unit: Optional[str] = None
    reference_range: Optional[list[float]] = None
    abnormal: Optional[bool] = None   # ✅ boolean

    date: Optional[Date] = None  


class ConfirmUploadRequest(BaseModel):
    temp_file_id: str
    lab_values: List[LabValueInput]


# ============================================================
# STEP 2: CONFIRM — user edited/confirmed values, now actually save
# ============================================================

@router.post("/confirm")
async def confirm_report(
    payload: ConfirmUploadRequest,
    current_patient: Patient = Depends(get_current_patient),
):
    file_path = os.path.join(UPLOAD_DIR, payload.temp_file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Temp file expired — please re-upload.")

    try:
        confirmed_labs = [lab.dict() for lab in payload.lab_values]

        result = save_confirmed_report(
            patient_id=str(current_patient.patient_id),
            file_path=file_path,
            confirmed_lab_values=confirmed_labs,
        )

        os.remove(file_path)

        if result.get("is_duplicate"):
            return result

        return {
            "message": "Report saved successfully",
            "document_id": str(result["document_id"])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# LIST + DETAIL — read back saved reports (documents / lab_results)
# NOTE: /list MUST be defined before /{document_id}, otherwise
# FastAPI tries to match "list" against the {document_id} pattern.
# ============================================================

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
            LEFT JOIN lab_results lr ON lr.document_id = d.document_id
            WHERE d.patient_id = :pid
            GROUP BY d.document_id, d.document_type, d.upload_date
            ORDER BY d.upload_date DESC
        """),
        {"pid": str(current_patient.patient_id)}
    ).fetchall()

    reports = []
    for r in rows:
        status = "Pending" if r.lab_count == 0 else ("Abnormal" if r.has_abnormal else "Normal")
        reports.append(ReportSummary(
            document_id=r.document_id,
            document_type=r.document_type,
            upload_date=r.upload_date,
            status=status,
            lab_count=r.lab_count,
        ))

    return reports


@router.get("/{document_id}", response_model=ReportDetail)
def get_report_detail(
    document_id: str,
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient),
):
    doc = db.execute(
        text("""
            SELECT document_id, document_type, upload_date
            FROM documents
            WHERE document_id = :did AND patient_id = :pid
        """),
        {"did": document_id, "pid": str(current_patient.patient_id)}
    ).fetchone()

    if doc is None:
        raise HTTPException(status_code=404, detail="Report not found")

    lab_rows = db.execute(
        text("""
            SELECT result_id, test_name, value, unit,
                   reference_low, reference_high, abnormal_flag, result_date
            FROM lab_results
            WHERE document_id = :did
            ORDER BY test_name
        """),
        {"did": document_id}
    ).fetchall()

    lab_values = [LabValueResponse(**row._mapping) for row in lab_rows]
    has_abnormal = any(lv.abnormal_flag is True for lv in lab_values)
    status = "Pending" if not lab_values else ("Abnormal" if has_abnormal else "Normal")

    return ReportDetail(
        document_id=doc.document_id,
        document_type=doc.document_type,
        upload_date=doc.upload_date,
        status=status,
        lab_values=lab_values,
    )
