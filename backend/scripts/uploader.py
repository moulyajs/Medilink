import io
import uuid
from storage import client, BUCKET
from database import SessionLocal
from sqlalchemy import text


def upload_file(file_path, patient_id):

    file_id = str(uuid.uuid4())
    filename = file_path.split("/")[-1]
    stored_name = f"{file_id}_{filename}"

    # Read file
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

    # Insert into documents table (FIXED)
    result = db.execute(
        text("""
        INSERT INTO documents
        (patient_id, document_type, upload_date, file_path)
        VALUES
        (:pid, :dtype, NOW(), :path)
        RETURNING document_id
        """),
        {
            "pid": patient_id,
            "dtype": "lab_report",
            "path": stored_name
        }
    )

    document_id = result.fetchone()[0]

    db.commit()
    db.close()

    return document_id, stored_name

##uploader.py