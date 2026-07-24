from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

router = APIRouter(
    prefix="/anomaly",
    tags=["Personal Baseline & Anomaly Detection"]
)


@router.get("/")
def get_patient_anomalies(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):

    patient_id = str(current_patient.patient_id)

    result = db.execute(
    text("""
        SELECT
            pa.test_name,
            pa.current_value,
            pa.personal_average,
            pa.personal_min,
            pa.personal_max,
            pa.personal_variability,
            pa.sample_count,
            pa.deviation,
            pa.percent_change,
            pa.trend,
            pa.detected_at,

            lr.reference_low,
            lr.reference_high,
            lr.unit

        FROM patient_anomalies pa

        JOIN lab_results lr
          ON pa.patient_id = lr.patient_id
         AND pa.test_name = lr.test_name
         AND pa.detected_at = lr.result_date

        WHERE pa.patient_id = :pid

        ORDER BY pa.detected_at DESC
    """),
    {"pid": patient_id}
)

    anomalies = []

    for row in result:
        anomalies.append(
    {
        "test_name": row.test_name,
        "current_value": row.current_value,

        "personal_average": row.personal_average,
        "personal_min": row.personal_min,
        "personal_max": row.personal_max,
        "personal_variability": row.personal_variability,
        "sample_count": row.sample_count,

        "reference_low": row.reference_low,
        "reference_high": row.reference_high,
        "unit": row.unit,

        "deviation": row.deviation,
        "percent_change": row.percent_change,
        "trend": row.trend,
        "detected_at": str(row.detected_at),
    }
)

    return anomalies