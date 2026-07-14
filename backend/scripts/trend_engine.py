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
# Main Function
# -----------------------------
def update_patient_trends(patient_id):

    print("\n==============================")
    print("TREND ENGINE STARTED")
    print("Patient ID:", patient_id)
    print("==============================")

    db = SessionLocal()

    try:

        # Get abnormal tests only
        abnormal_query = text("""
            SELECT DISTINCT test_name
            FROM lab_results
            WHERE patient_id = :patient_id
              AND abnormal_flag = true
        """)

        abnormal_tests = db.execute(
            abnormal_query,
            {"patient_id": patient_id}
        ).fetchall()

        if not abnormal_tests:
            print("\nNo abnormal lab tests found.")
            return

        print("\nAbnormal Tests Found:")

        for row in abnormal_tests:

            test_name = row.test_name
            print(f"\n{test_name}")

            # Fetch complete history of this test
            history_query = text("""
                SELECT
                    value,
                    result_date,
                    reference_low,
                    reference_high
                FROM lab_results
                WHERE patient_id = :patient_id
                  AND test_name = :test_name
                ORDER BY result_date
            """)

            history = db.execute(
                history_query,
                {
                    "patient_id": patient_id,
                    "test_name": test_name
                }
            ).fetchall()

            if len(history) == 0:
                continue

            values = [row.value for row in history]

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
                len(values)
            )

            print("------------------------------------")
            print("Test Name     :", test_name)
            print("Values        :", values)
            print("Latest Value  :", latest)
            print("Status        :", status)
            print("Delta         :", delta)
            print("Slope         :", slope)
            print("Trend         :", trend)
            print("Data Points   :", len(values))
    
        db.commit() 
    finally:
        db.close()

def save_trend(
        db,
        patient_id,
        test_name,
        latest_value,
        delta,
        slope,
        trend,
        status,
        data_points):

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

        ON CONFLICT
        (patient_id,test_name)

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

            "points": data_points

        }

    )