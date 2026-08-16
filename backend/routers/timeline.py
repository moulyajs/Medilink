from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"]
)

@router.get("/")
def get_timeline(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    patient_id = str(current_patient.patient_id)

    try:

        result = db.execute(
            text("""
                SELECT
                    event_id,
                    patient_id,
                    event_type,
                    event_date,
                    source_document,
                    summary
                FROM timeline_events
                WHERE patient_id = :pid
                ORDER BY event_date DESC
            """),
            {"pid": patient_id}
        )

        timeline = []

        for row in result:
            timeline.append(
                {
                    "id": str(row.event_id),
                    "patient_id": str(row.patient_id),
                    "document_type": row.event_type,
                    "event_date": str(row.event_date),
                    "summary": row.summary,
                    "source_document": (
                        str(row.source_document)
                        if row.source_document
                        else None
                    ),
                }
            )

        return timeline

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )