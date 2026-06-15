from database import SessionLocal
from sqlalchemy import text
from database import DB_URL

print("TIMELINE DB URL =", DB_URL)

def get_timeline(patient_id):

    db = SessionLocal()

    result = db.execute(
        text("""
        SELECT
            t.id,
            t.record_id,
            t.event_date,
            t.event_type,
            t.short_summary,
            f.file_name,
            f.file_path

        FROM timeline t

        LEFT JOIN medical_records mr
            ON t.record_id = mr.id

        LEFT JOIN files f
            ON mr.file_id = f.id

        WHERE t.patient_id = :pid

        ORDER BY t.event_date DESC

        LIMIT 3
        """),
        {"pid": patient_id}
    )

    timeline = []

    for row in result:
        timeline.append({
            "id": row.id,
            "record_id": row.record_id,
            "date": str(row.event_date),
            "type": row.event_type,
            "summary": row.short_summary,
            "file_name": row.file_name,
            "file_path": row.file_path
        })

    db.close()

    return timeline