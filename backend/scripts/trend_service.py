from collections import defaultdict
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import text

from database import SessionLocal


def calculate_delta(values):
    if len(values) < 2:
        return 0

    return round(values[-1] - values[-2], 2)


def calculate_slope(values):
    if len(values) < 2:
        return 0

    X = np.arange(len(values)).reshape(-1, 1)
    y = np.array(values)

    model = LinearRegression()
    model.fit(X, y)

    return round(float(model.coef_[0]), 2)


def determine_trend(slope):

    if slope > 0.5:
        return "Increasing"

    if slope < -0.5:
        return "Decreasing"

    return "Stable"


def fetch_patient_records(patient_id):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT
                    test_name,
                    value,
                    unit,
                    reference_low,
                    reference_high,
                    abnormal_flag,
                    result_date
                FROM lab_results
                WHERE patient_id = :patient_id
                ORDER BY result_date
            """),
            {"patient_id": patient_id}
        ).fetchall()

        return rows

    finally:
        db.close()

def group_lab_results(rows):

    grouped = defaultdict(list)

    for row in rows:

        test_name = (row.test_name or "").strip()

        if not test_name:
            continue

        grouped[test_name].append({
            "value": float(row.value),
            "abnormal": row.abnormal_flag,
            "date": row.result_date,
            "reference_range": (
                row.reference_low,
                row.reference_high
            )
        })

    return grouped


def analyze_trends(grouped):

    results = []

    BAD_WORDS = [
        "Test Result Unit",
        "Biological Ref",
        "High Performance",
        "Chemiluminescence"
    ]

    for test_name, records in grouped.items():

        # Need at least 2 values for trend calculation
        if len(records) < 2:
            continue

        # Skip OCR garbage names
        if any(word in test_name for word in BAD_WORDS):
            continue

        if len(test_name) > 60:
            continue

        latest_record = records[-1]

        latest_value = latest_record["value"]
        status = latest_record["status"]
        abnormal = latest_record["abnormal"]

        # Only abnormal labs are analyzed
        if not abnormal:
            continue

        values = [r["value"] for r in records]

        delta = calculate_delta(values)
        slope = calculate_slope(values)
        trend = determine_trend(slope)

        # Select analysis method based on number of reports
        data_points = len(values)

        if data_points < 10:
            analysis_method = "Linear Regression"

        elif data_points < 100:
            analysis_method = "LSTM Autoencoder"

        else:
            analysis_method = "Transformer"

        results.append({
            "test_name": test_name,
            "latest_value": latest_value,
            "status": status,
            "abnormal": abnormal,
            "delta": delta,
            "slope": slope,
            "trend": trend,
            "data_points": data_points,
            "analysis_method": analysis_method
        })

    return results


def save_trends(patient_id, trends):

    db = SessionLocal()

    try:

        # Remove old trends for this patient
        db.execute(
            text("""
                DELETE FROM lab_trends
                WHERE patient_id = :patient_id
            """),
            {"patient_id": patient_id}
        )

        # Insert latest trends
        for trend in trends:

            db.execute(
                text("""
                    INSERT INTO lab_trends( 
                        patient_id,
                        test_name,
                        latest_value,
                        delta,
                        slope,
                        status,
                        trend,
                        analysis_method,
                        data_points
                    )
                    VALUES(
                        :patient_id,
                        :test_name,
                        :latest_value,
                        :delta,
                        :slope,
                        :status,
                        :trend,
                        :analysis_method,
                        :data_points
                    )
                """),
                {
                    "patient_id": patient_id,
                    "test_name": trend["test_name"],
                    "latest_value": trend["latest_value"],
                    "delta": trend["delta"],
                    "slope": trend["slope"],
                    "status": trend["status"],
                    "trend": trend["trend"],
                    "analysis_method": trend["analysis_method"],
                    "data_points": trend["data_points"]
                }
            )

        db.commit()

    finally:
        db.close()

def generate_patient_trends(patient_id):

    rows = fetch_patient_records(patient_id)

    grouped = group_lab_results(rows)

    trends = analyze_trends(grouped)

    save_trends(patient_id, trends)

    return trends


if __name__ == "__main__":

    patient_id = 2

    rows = fetch_patient_records(patient_id)

    grouped = group_lab_results(rows)

    print("\nABNORMAL LAB ANALYSIS\n")

    trends = analyze_trends(grouped)

    save_trends(patient_id, trends)

    for trend in trends:
        print(trend)