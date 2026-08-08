import uuid
from sqlalchemy import text
from database import SessionLocal
from scripts.baseline_engine import update_patient_baselines
from scripts.trend_engine import update_patient_trends
from scripts.anomaly_detection import detect_patient_anomalies
from scripts.anomaly_saver import save_patient_anomalies

# ===============================
# VERIFY PATIENT
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
# SAVE MEDICAL RECORD
# ===============================

def save_medical_record(
    patient_id,
    file_id,
    document_type,
    labs,
    clinical_facts
):
    """
    Keeps same function signature used by app.py
    Stores extracted labs into lab_results table.
    """

    db = SessionLocal()

    for lab in labs:

        test_name = (lab.get("test_name") or lab.get("test") or "").strip().upper()

        if not test_name:
            continue

        if lab.get("value") is None:
            continue

        result_id = str(uuid.uuid4())

        ref_low = None
        ref_high = None

        ref_range = lab.get("reference_range")

        if ref_range and len(ref_range) >= 2:
            ref_low = ref_range[0]
            ref_high = ref_range[1]

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
                :docid,
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
                "docid": file_id,
                "name": test_name,
                "cat": "LAB",
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

# Update baseline and trends
    update_patient_baselines(patient_id)
    update_patient_trends(patient_id)

    db.close()

    print("✅ Lab results saved")

    return file_id


# ===============================
# OPTIONAL
# ===============================

def save_patient(*args, **kwargs):
    pass