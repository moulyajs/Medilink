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
        INSERT INTO timeline
        (patient_id, record_id, event_date, event_type, short_summary)
        VALUES
        (:pid, :rid, NOW(), :etype, :summary)
        """),
        {
            "pid": patient_id,
            "rid": record_id,
            "etype": event_type,
            "summary": short_summary[:250]
        }
    )

    db.commit()
    db.close()
