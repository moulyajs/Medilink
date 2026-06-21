import json
from sqlalchemy import text
from database import SessionLocal


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

    db = SessionLocal()

    result = db.execute(
        text("""
        INSERT INTO medical_records
        (
            patient_id,
            file_id,
            document_type,
            lab_results,
            clinical_facts
        )
        VALUES
        (
            :pid,
            :fid,
            :dtype,
            CAST(:labs AS jsonb),
            CAST(:facts AS jsonb)
        )
        RETURNING id
        """),
        {
            "pid": patient_id,
            "fid": file_id,
            "dtype": document_type,
            "labs": json.dumps(labs, default=str),
            "facts": json.dumps(clinical_facts, default=str)
        }
    )

    medical_record_id = result.fetchone()[0]

    db.commit()
    db.close()

    return medical_record_id


# ===============================
# OPTIONAL - KEEP FOR FUTURE
# ===============================
def save_patient(*args, **kwargs):
    """
    Not used currently.
    Existing patients are already stored.
    """
    pass


def save_lab_results(*args, **kwargs):
    """
    Not used currently.

    We are storing lab data inside:
    medical_records.lab_results (JSONB)

    instead of a separate lab_results table.
    """
    pass