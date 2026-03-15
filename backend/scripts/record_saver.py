import uuid
from sqlalchemy import text
from database import SessionLocal


def save_patient(patient_id, dob=None, gender=None):

    db = SessionLocal()

    db.execute(
        text("""
        INSERT INTO patients (patient_id, dob, gender)
        VALUES (:pid, :dob, :gender)
        ON CONFLICT (patient_id) DO NOTHING
        """),
        {
            "pid": patient_id,
            "dob": dob,
            "gender": gender
        }
    )

    db.commit()
    db.close()


def save_lab_results(patient_id, document_id, labs):

    db = SessionLocal()

    for lab in labs:

        # Handle both formats (test_name or test)
        test_name = lab.get("test_name") or lab.get("test")

        # Skip invalid OCR rows
        if not test_name or lab.get("value") is None:
            print("⚠ Skipping invalid lab row:", lab)
            continue

        result_id = str(uuid.uuid4())

        # Handle reference ranges
        ref_low = lab.get("ref_low")
        ref_high = lab.get("ref_high")

        if "reference_range" in lab and lab["reference_range"]:
            ref_low, ref_high = lab["reference_range"]

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
                "cat": lab.get("category", "lab"),
                "value": lab.get("value"),
                "unit": lab.get("unit"),
                "low": ref_low,
                "high": ref_high,
                "flag": lab.get("abnormal"),
                "date": lab.get("date")
            }
        )

    db.commit()
    db.close()