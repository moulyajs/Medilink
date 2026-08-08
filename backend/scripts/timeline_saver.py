from database import SessionLocal
from sqlalchemy import text

def add_timeline_event(
    patient_id,
    document_id,
    event_type,
    summary
):

    db = SessionLocal()

    db.execute(
        text("""
        INSERT INTO timeline_events
        (
            patient_id,
            event_type,
            event_date,
            source_document,
            summary
        )
        VALUES
        (
            :pid,
            :etype,
            NOW(),
            :docid,
            :summary
        )
        """),
        {
            "pid": patient_id,
            "etype": event_type,
            "docid": str(document_id),
            "summary": str(summary)
        }
    )

    db.commit()
    db.close()

    print("✅ Timeline event saved")