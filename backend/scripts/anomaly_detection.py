from sqlalchemy import text
from database import SessionLocal


def detect_patient_anomalies(patient_id, current_labs):

    db = SessionLocal()

    anomalies = []

    try:

        for lab in current_labs:

            test_name = (lab.get("test") or "").strip().upper()
            current_value = lab.get("value")

            if test_name is None or current_value is None:
                continue

            # ---------------------------------------
            # Fetch patient's baseline
            # ---------------------------------------
            baseline = db.execute(
                text("""
                    SELECT
                        personal_average,
                        personal_min,
                        personal_max,
                        personal_variability,
                        sample_count
                    FROM personal_baseline
                    WHERE patient_id = :pid
                      AND test_name = :test
                """),
                {
                    "pid": patient_id,
                    "test": test_name
                }
            ).fetchone()

            if baseline is None:
                continue

            # Need at least two previous reports
            if baseline.sample_count < 2:
                continue

            deviation = current_value - baseline.personal_average

            pct_change = (
                (deviation / baseline.personal_average) * 100
                if baseline.personal_average != 0
                else 0
            )

            if abs(pct_change) >= 20:

                trend = "UP" if deviation > 0 else "DOWN"

                anomalies.append({
                    "test_name": test_name,
                    "current_value": current_value,
                    "baseline": baseline.personal_average,
                    "baseline_min": baseline.personal_min,
                    "baseline_max": baseline.personal_max,
                    "variability": baseline.personal_variability,
                    "sample_count": baseline.sample_count,
                    "deviation": round(deviation, 2),
                    "percent_change": round(pct_change, 2),
                    "trend": trend,
                    "detected_at": lab.get("date")
                })

        return anomalies

    finally:
        db.close()