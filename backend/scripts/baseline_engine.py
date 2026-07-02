import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
import uuid
import statistics

from sqlalchemy import text
from database import SessionLocal

def get_history(patient_id, test_name):
    """
    Returns all historical values for a patient's lab test.
    """

    db = SessionLocal()

    result = db.execute(
        text("""
            SELECT value
            FROM lab_results
            WHERE patient_id = :pid
              AND test_name = :test
            ORDER BY result_date
        """),
        {
            "pid": patient_id,
            "test": test_name
        }
    )

    values = [row.value for row in result if row.value is not None]

    db.close()

    return values

import statistics

def calculate_baseline(values):
    """
    Calculates the patient's personal baseline statistics.
    """

    if len(values) == 0:
        return None

    baseline = {
        "average": round(statistics.mean(values), 2),
        "minimum": min(values),
        "maximum": max(values),
        "variability": round(
            statistics.stdev(values), 2
        ) if len(values) > 1 else 0.0,
        "sample_count": len(values)
    }

    return baseline

def save_baseline(patient_id, test_name, baseline):
    """
    Inserts or updates the personal baseline for a patient's lab test.
    """

    db = SessionLocal()

    db.execute(
        text("""
            INSERT INTO personal_baseline (
                baseline_id,
                patient_id,
                test_name,
                personal_average,
                personal_min,
                personal_max,
                personal_variability,
                sample_count
            )
            VALUES (
                :bid,
                :pid,
                :test,
                :avg,
                :min,
                :max,
                :var,
                :count
            )
            ON CONFLICT (patient_id, test_name)
            DO UPDATE SET
                personal_average = EXCLUDED.personal_average,
                personal_min = EXCLUDED.personal_min,
                personal_max = EXCLUDED.personal_max,
                personal_variability = EXCLUDED.personal_variability,
                sample_count = EXCLUDED.sample_count,
                last_updated = NOW();
        """),
        {
            "bid": str(uuid.uuid4()),
            "pid": patient_id,
            "test": test_name,
            "avg": baseline["average"],
            "min": baseline["minimum"],
            "max": baseline["maximum"],
            "var": baseline["variability"],
            "count": baseline["sample_count"]
        }
    )

    db.commit()
    db.close()

def update_patient_baselines(patient_id):
    """
    Recalculates the baseline for every lab test of a patient.
    """

    db = SessionLocal()

    result = db.execute(
        text("""
            SELECT DISTINCT test_name
            FROM lab_results
            WHERE patient_id = :pid
        """),
        {
            "pid": patient_id
        }
    )

    tests = [row.test_name for row in result]

    db.close()

    for test in tests:
        values = get_history(patient_id, test)

        baseline = calculate_baseline(values)

        if baseline:
            save_baseline(patient_id, test, baseline)

            print(f"✅ Updated baseline for {test}")