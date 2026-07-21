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

from database import get_db
from utils.dependencies import get_current_patient
from models.patient import Patient

from scripts.app import process_document   # <-- Add this

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
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
            filename
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("🚀 Starting AI pipeline...")

        process_document(
            file_path=file_path,
            patient_id=str(current_patient.patient_id),
        )

        print("✅ AI pipeline completed")

        return {
            "message": "File uploaded and processed successfully",
            "patient_id": str(current_patient.patient_id),
            "file_path": file_path,
            "filename": filename,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )