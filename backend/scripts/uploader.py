import io
import uuid
from storage import client, BUCKET
from database import SessionLocal
from sqlalchemy import text


def upload_file(file_path, patient_id):

    file_id = str(uuid.uuid4())
    filename = file_path.split("/")[-1]
    stored_name = f"{file_id}_{filename}"

    with open(file_path, "rb") as f:
        content = f.read()

    stream = io.BytesIO(content)

    # Upload to MinIO
    client.put_object(
        BUCKET,
        stored_name,
        stream,
        length=len(content)
    )

    db = SessionLocal()

    result = db.execute(
        text("""
        INSERT INTO files
        (patient_id, file_name, file_path, status)
        VALUES
        (:pid, :name, :path, 'uploaded')
        RETURNING id
        """),
        {
            "pid": patient_id,
            "name": filename,
            "path": stored_name
        }
    )

    file_db_id = result.fetchone()[0]

    db.commit()
    db.close()

    return file_db_id, stored_name
