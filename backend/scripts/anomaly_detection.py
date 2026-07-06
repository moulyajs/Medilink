from sqlalchemy import text
from database import SessionLocal
from rapidfuzz import fuzz

def is_same_test(a, b):
    if not a or not b:
        return False

    a = a.lower().strip()
    b = b.lower().strip()

    return fuzz.partial_ratio(a, b) >= 90

def detect_patient_anomalies(patient_id, current_labs):

    db = SessionLocal()

    anomalies = []

    for lab in current_labs:

        test_name = lab.get("test")
        current_value = lab.get("value")

        if test_name is None or current_value is None:
            continue

        # -----------------------------
        # Fetch historical values
        # -----------------------------
        # -----------------------------
# Fetch ALL historical values
# -----------------------------
        all_rows = db.execute(
            text("""
                SELECT test_name, value, result_date
                FROM lab_results
                WHERE patient_id = :pid
                AND value IS NOT NULL
                ORDER BY result_date
            """),
            {
                "pid": patient_id
            }
        ).fetchall()

        rows = []

        for r in all_rows:
            if is_same_test(test_name, r.test_name):
                rows.append(r)
        print("\nSearching:", test_name)
        print("Rows found:", len(rows))

        for r in rows:
            print(r.value, r.result_date)
        history = [r.value for r in rows]

        # Ignore current upload if already inserted
        if len(history) > 0:
            history = history[:-1]

        # Need at least 2 previous reports
        if len(history) < 2:
            continue

        baseline = sum(history) / len(history)

        deviation = current_value - baseline

        pct_change = (deviation / baseline) * 100 if baseline != 0 else 0

        if abs(pct_change) >= 20:

            trend = "UP"

            if deviation < 0:
                trend = "DOWN"

            anomalies.append({

                "test_name": test_name,

                "current_value": current_value,

                "baseline": round(baseline,2),

                "percent_change": round(pct_change,2),

                "trend": trend,

                "history": history

            })

    db.close()

    return anomalies