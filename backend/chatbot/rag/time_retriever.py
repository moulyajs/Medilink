from .vector_store import (
    get_lab_chunks,
    get_all_patient_chunks
)
from sqlalchemy import text
from database import SessionLocal

from scripts.trend_engine import (
    calculate_delta,
    calculate_slope,
    determine_trend,
    range_check,
)

def get_lab_trend(patient_id, test_name):
    print("\nEntered get_lab_trend()")
    print("Patient:", patient_id)
    print("Test:", test_name)
    db = SessionLocal()

    try:

        # ----------------------------------
        # 1. Check if precomputed trend exists
        # ----------------------------------

        trend = db.execute(
            text("""
            SELECT
                latest_value,
                delta,
                slope,
                trend,
                status,
                data_points
            FROM lab_trends
            WHERE patient_id = :pid
              AND test_name = :test
            """),
            {
                "pid": patient_id,
                "test": test_name,
            },
        ).mappings().first()
        print("\nTrend from lab_trends:")
        print(trend)

        if trend:
            print("Using precomputed trend")
            return dict(trend)
        print("No precomputed trend found.")
        print("Computing from lab_results...")
        # ----------------------------------
        # 2. Otherwise compute on demand
        # ----------------------------------

        rows = db.execute(
            text("""
            SELECT
                value,
                result_date,
                reference_low,
                reference_high
            FROM lab_results
            WHERE patient_id = :pid
              AND test_name = :test
            ORDER BY result_date
            """),
            {
                "pid": patient_id,
                "test": test_name,
            },
        ).mappings().all()

        if not rows:
            return None

        values = [r["value"] for r in rows]

        latest = rows[-1]["value"]
        low = rows[-1]["reference_low"]
        high = rows[-1]["reference_high"]

        delta = calculate_delta(values)
        slope = calculate_slope(values)
        trend_name = determine_trend(slope)
        status = range_check(latest, low, high)
        print("\nComputed Trend")
        print("Values:", values)
        print("Latest:", latest)
        print("Delta:", delta)
        print("Slope:", slope)
        print("Trend:", trend_name)
        print("Status:", status)
        
        return {
            "latest_value": latest,
            "delta": delta,
            "slope": slope,
            "trend": trend_name,
            "status": status,
            "data_points": len(values),
        }
        
    finally:
        db.close()


def get_latest_lab(
    patient_id,
    test_name
):

    chunks = get_lab_chunks(
        patient_id,
        test_name
    )

    if not chunks:
        return None

    chunks.sort(
        key=lambda c:
            c.payload.get(
                "report_date",
                ""
            ),
        reverse=True
    )

    return chunks[0]

def get_lab_history(
    patient_id,
    test_name
):

    chunks = get_lab_chunks(
        patient_id,
        test_name
    )

    history = []

    for c in chunks:

        md = c.payload.get(
            "metadata",
            {}
        )

        history.append({
            "date": c.payload.get("report_date"),
            "value": md.get("value"),
            "abnormal": md.get("abnormal", False),
        })

    history.sort(
        key=lambda x: x["date"]
    )

    return history
def get_abnormal_labs(patient_id):

    chunks = get_all_patient_chunks(
        patient_id
    )

    abnormal = []

    for c in chunks:

        md = c.payload.get(
            "metadata",
            {}
        )

        if md.get("abnormal", False):
            abnormal.append(c)

    return abnormal