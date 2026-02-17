from database import SessionLocal
from sqlalchemy import text
import json


def save_medical_record(
    patient_id,
    file_id,
    doc_type,
    demographics,
    prescriptions,
    labs,
    clinical_facts,
    summary,
    explanation
):

    db = SessionLocal()

    result = db.execute(
        text("""
        INSERT INTO medical_records
        (
            patient_id,
            file_id,
            document_type,
            demographics,
            prescriptions,
            lab_results,
            clinical_facts,
            clinical_summary,
            patient_explanation
        )
        VALUES
        (
            :pid, :fid, :dtype,
            :demo, :pres, :labs, :facts,
            :summary, :explain
        )
        RETURNING id
        """),
        {
            "pid": patient_id,
            "fid": file_id,
            "dtype": doc_type,

            "demo": json.dumps(demographics),
            "pres": json.dumps(prescriptions),
            "labs": json.dumps(labs),
            "facts": json.dumps(clinical_facts),

            "summary": summary,
            "explain": explanation
        }
    )

    record_id = result.fetchone()[0]

    db.commit()
    db.close()

    return record_id
