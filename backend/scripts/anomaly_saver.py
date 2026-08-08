import uuid

from sqlalchemy import text
from database import SessionLocal


def save_patient_anomalies(patient_id, anomalies, current_labs):

    db = SessionLocal()

    try:

        # ---------------------------------------
        # Get uploaded test names
        # ---------------------------------------
        uploaded_tests = list({
            lab["test"]
            for lab in current_labs
            if lab.get("test")
        })

        # ---------------------------------------
        # Remove previous anomalies only for
        # uploaded tests
        # ---------------------------------------
        if uploaded_tests:

            placeholders = ", ".join(
                f":test{i}" for i in range(len(uploaded_tests))
            )

            params = {"pid": patient_id}

            for i, test in enumerate(uploaded_tests):
                params[f"test{i}"] = test

            db.execute(
                text(f"""
                    DELETE
                    FROM patient_anomalies
                    WHERE patient_id = :pid
                    AND test_name IN ({placeholders})
                """),
                params
            )

        # ---------------------------------------
        # Insert newly detected anomalies
        # ---------------------------------------
        for anomaly in anomalies:

            db.execute(
                text("""
                    INSERT INTO patient_anomalies
                    (
                        anomaly_id,
                        patient_id,
                        test_name,
                        current_value,
                        personal_average,
                        personal_min,
                        personal_max,
                        personal_variability,
                        sample_count,
                        deviation,
                        percent_change,
                        trend,
                        detected_at,
                        last_updated
                    )
                    VALUES
                    (
                        :id,
                        :pid,
                        :test,
                        :current,
                        :avg,
                        :min,
                        :max,
                        :var,
                        :count,
                        :deviation,
                        :percent,
                        :trend,
                        :date,
                        NOW()
                    )
                """),
                {
                    "id": str(uuid.uuid4()),
                    "pid": patient_id,
                    "test": anomaly["test_name"],
                    "current": anomaly["current_value"],
                    "avg": anomaly["baseline"],
                    "min": anomaly["baseline_min"],
                    "max": anomaly["baseline_max"],
                    "var": anomaly["variability"],
                    "count": anomaly["sample_count"],
                    "deviation": anomaly["deviation"],
                    "percent": anomaly["percent_change"],
                    "trend": anomaly["trend"],
                    "date": anomaly["detected_at"]
                }
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()