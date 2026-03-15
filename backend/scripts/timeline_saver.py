from database import SessionLocal
from sqlalchemy import text


def add_timeline_event(
    patient_id,
    record_id,
    event_type,
    short_summary
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
            :doc,
            :summary
        )
        """),
        {
            "pid": patient_id,
            "etype": event_type,
            "doc": record_id,
            "summary": short_summary
        }
    )

    db.commit()
    db.close()

#timeline_saver.py