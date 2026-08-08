from database import SessionLocal
from sqlalchemy import text
from database import DB_URL

print("TIMELINE DB URL =", DB_URL)


def get_timeline(patient_id):

    db = SessionLocal()

    result = db.execute(
        text("""
        SELECT
            te.event_id,
            te.event_date,
            te.event_type,
            te.summary,
            d.document_id,
            d.file_path

        FROM timeline_events te

        LEFT JOIN documents d
            ON te.source_document = d.document_id

        WHERE te.patient_id = :pid

        ORDER BY te.event_date DESC

        LIMIT 3
        """),
        {"pid": patient_id}
    )

    timeline = []

    for row in result:
        timeline.append({
            "id": str(row.event_id),
            "document_id": str(row.document_id) if row.document_id else None,
            "date": str(row.event_date),
            "type": row.event_type,
            "summary": row.summary,
            "file_path": row.file_path
        })

    db.close()

    return timeline