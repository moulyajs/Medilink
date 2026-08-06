import uuid
from sqlalchemy import text
from database import SessionLocal
from scripts.baseline_engine import update_patient_baselines
from scripts.trend_engine import update_patient_trends
from scripts.anomaly_detection import detect_patient_anomalies
from scripts.anomaly_saver import save_patient_anomalies

# ===============================
# SAVE PATIENT
# ===============================

def verify_patient(patient_id):
    db = SessionLocal()

    patient = db.execute(
        text("""
            SELECT patient_id
            FROM patients
            WHERE patient_id = :pid
        """),
        {"pid": patient_id}
    ).fetchone()

    db.close()

    if patient is None:
        raise Exception(f"Patient {patient_id} not found")


# ===============================
# SAVE LAB RESULTS
# ===============================
def save_lab_results(patient_id, document_id, labs):

    db = SessionLocal()

    for lab in labs:

        test_name = (lab.get("test_name") or lab.get("test") or "").strip().upper()

        if not test_name or lab.get("value") is None:
            print("⚠ Skipping:", lab)
            continue

        result_id = str(uuid.uuid4())

        ref_low = None
        ref_high = None

        if "reference_range" in lab and lab["reference_range"]:
            ref_low, ref_high = lab["reference_range"]
        print(lab)
        db.execute(
            text("""
            INSERT INTO lab_results
            (
                result_id,
                patient_id,
                document_id,
                test_name,
                test_category,
                value,
                unit,
                reference_low,
                reference_high,
                abnormal_flag,
                result_date
            )
            VALUES
            (
                :rid,
                :pid,
                :doc,
                :name,
                :cat,
                :value,
                :unit,
                :low,
                :high,
                :flag,
                :date
            )
            """),
            {
                "rid": result_id,
                "pid": patient_id,
                "doc": document_id,
                "name": test_name,
                "cat": "lab",
                "value": lab.get("value"),
                "unit": lab.get("unit"),
                "low": ref_low,
                "high": ref_high,
                "flag": lab.get("abnormal"),
                "date": lab.get("date")  # ✅ now properly filled
            }
        )
        

    db.commit()
    # Ensure normalized names are used by anomaly detection
    for lab in labs:
        test_name = (lab.get("test_name") or lab.get("test") or "").strip().upper()
        lab["test"] = test_name

    # Detect anomalies using the previous baseline
    anomalies = detect_patient_anomalies(
        patient_id,
        labs
    )

    save_patient_anomalies(
        patient_id,
        anomalies,
        labs
    )

    # Now update baseline and trends to include the new report
    update_patient_baselines(patient_id)
    update_patient_trends(patient_id)
    db.close()