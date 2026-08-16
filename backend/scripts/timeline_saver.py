from database import SessionLocal
from sqlalchemy import text


def add_timeline_event(
    patient_id,
    document_id,
    event_type,
    summary,
    event_date=None
):
    """
    Save a timeline event.

    Date priority:
    1. Date extracted from the medical report
    2. Upload date if the report does not contain a date
    """

    db = SessionLocal()

    try:

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
                    COALESCE(:event_date, NOW()),
                    :docid,
                    :summary
                )
            """),
            {
                "pid": patient_id,
                "etype": event_type,
                "event_date": event_date,
                "docid": str(document_id),
                "summary": str(summary)
            }
        )

        db.commit()

        print("✅ Timeline event saved")

        if event_date:
            print(
                "📅 Using report date:",
                event_date
            )
        else:
            print(
                "📅 No report date found - using upload date"
            )

    except Exception as e:

        db.rollback()

        print(
            "❌ Timeline save failed:",
            e
        )

        raise

    finally:

        db.close()