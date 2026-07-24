from sqlalchemy import text
from database import SessionLocal

import numpy as np
from sklearn.linear_model import LinearRegression


# -----------------------------
# Calculate Delta
# -----------------------------
def calculate_delta(values):
    if len(values) < 2:
        return None
    return round(values[-1] - values[-2], 2)


# -----------------------------
# Calculate Linear Regression Slope
# -----------------------------
def calculate_slope(values):
    if len(values) < 2:
        return None

    X = np.arange(len(values)).reshape(-1, 1)
    y = np.array(values)

    model = LinearRegression()
    model.fit(X, y)

    return round(float(model.coef_[0]), 4)


# -----------------------------
# Determine Trend
# -----------------------------
def determine_trend(slope):

    if slope is None:
        return "Insufficient Data"

    if slope > 0.05:
        return "Increasing"

    elif slope < -0.05:
        return "Decreasing"

    else:
        return "Stable"


# -----------------------------
# Range Check
# -----------------------------
def range_check(value, low, high):

    if low is not None and value < low:
        return "LOW"

    if high is not None and value > high:
        return "HIGH"

    return "NORMAL"


# -----------------------------
# Save Trend
# -----------------------------
def save_trend(
    db,
    patient_id,
    test_name,
    latest_value,
    delta,
    slope,
    trend,
    status,
    data_points,
):

    db.execute(
        text("""
        INSERT INTO lab_trends
        (
            patient_id,
            test_name,
            latest_value,
            delta,
            slope,
            trend,
            status,
            data_points
        )
        VALUES
        (
            :pid,
            :test,
            :latest,
            :delta,
            :slope,
            :trend,
            :status,
            :points
        )
        ON CONFLICT (patient_id, test_name)
        DO UPDATE SET
            latest_value = EXCLUDED.latest_value,
            delta = EXCLUDED.delta,
            slope = EXCLUDED.slope,
            trend = EXCLUDED.trend,
            status = EXCLUDED.status,
            data_points = EXCLUDED.data_points,
            updated_at = NOW()
        """),
        {
            "pid": patient_id,
            "test": test_name,
            "latest": latest_value,
            "delta": delta,
            "slope": slope,
            "trend": trend,
            "status": status,
            "points": data_points,
        },
    )


# -----------------------------
# Update Trends for ONE Patient
# -----------------------------
def update_patient_trends(patient_id):

    print("\n" + "=" * 50)
    print("TREND ENGINE STARTED")
    print("Patient:", patient_id)
    print("=" * 50)

    db = SessionLocal()

    try:

        # Remove previous trends
        db.execute(
            text("""
            DELETE FROM lab_trends
            WHERE patient_id = :patient_id
            """),
            {"patient_id": patient_id},
        )

        abnormal_tests = db.execute(
            text("""
            SELECT DISTINCT test_name
            FROM lab_results
            WHERE patient_id = :patient_id
              AND abnormal_flag = true
            """),
            {"patient_id": patient_id},
        ).fetchall()

        print(f"Abnormal Tests Found: {len(abnormal_tests)}")

        if not abnormal_tests:
            db.commit()
            print("No abnormal tests found.")
            return

        for row in abnormal_tests:

            test_name = row.test_name

            history = db.execute(
                text("""
                SELECT
                    value,
                    result_date,
                    reference_low,
                    reference_high
                FROM lab_results
                WHERE patient_id = :patient_id
                  AND test_name = :test_name
                ORDER BY result_date
                """),
                {
                    "patient_id": patient_id,
                    "test_name": test_name,
                },
            ).fetchall()

            if not history:
                continue

            values = [r.value for r in history]

            latest = history[-1].value
            low = history[-1].reference_low
            high = history[-1].reference_high

            status = range_check(latest, low, high)
            delta = calculate_delta(values)
            slope = calculate_slope(values)
            trend = determine_trend(slope)

            save_trend(
                db,
                patient_id,
                test_name,
                latest,
                delta,
                slope,
                trend,
                status,
                len(values),
            )

            print(f"Saved trend: {test_name}")

        db.commit()
        print("Trend generation completed.")

    finally:
        db.close()


# -----------------------------
# Update Trends for ALL Patients
# -----------------------------
def update_all_patient_trends():

    db = SessionLocal()

    try:

        patients = db.execute(
            text("""
            SELECT DISTINCT patient_id
            FROM lab_results
            """)
        ).fetchall()

    finally:
        db.close()

    print(f"\nFound {len(patients)} patients\n")

    for row in patients:
        update_patient_trends(row.patient_id)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    update_all_patient_trends()