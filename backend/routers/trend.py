from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

router = APIRouter(
    prefix="/trend",
    tags=["Trend"]
)


@router.get("/trend-analysis")
def get_trend_analysis(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    patient_id = str(current_patient.patient_id)

    try:
        result = db.execute(
            text("""
                SELECT
                    test_name,
                    latest_value,
                    delta,
                    slope,
                    trend,
                    status,
                    data_points
                FROM lab_trends
                WHERE patient_id = :pid
                ORDER BY test_name
            """),
            {"pid": patient_id},
        )

        trends = []

        for row in result:

            history_result = db.execute(
                text("""
                    SELECT
                        result_date,
                        value
                    FROM lab_results
                    WHERE patient_id = :pid
                      AND test_name = :test
                    ORDER BY result_date
                """),
                {
                    "pid": patient_id,
                    "test": row.test_name,
                },
            )

            history = []

            for h in history_result:
                history.append(
                    {
                        "date": str(h.result_date),
                        "value": h.value,
                    }
                )

            trends.append(
                {
                    "test_name": row.test_name,
                    "latest_value": row.latest_value,
                    "delta": row.delta,
                    "slope": row.slope,
                    "trend": row.trend,
                    "status": row.status,
                    "data_points": row.data_points,
                    "history": history,
                }
            )

        return trends

    finally:
        db.close()