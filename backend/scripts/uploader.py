import io
import os
import uuid

from storage import client, BUCKET
from database import SessionLocal
from sqlalchemy import text


def upload_file(file_path, patient_id):
    """
    Upload file to MinIO and save metadata in PostgreSQL.
    Returns:
        file_id (int)
        stored_name (str)
    """

    # Generate unique file name
    file_uuid = str(uuid.uuid4())
    filename = os.path.basename(file_path)
    stored_name = f"{file_uuid}_{filename}"

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

    # Save file metadata in PostgreSQL
    db = SessionLocal()

    result = db.execute(
        text("""
        INSERT INTO files
        (
            patient_id,
            file_name,
            file_path,
            file_type,
            status
        )
        VALUES
        (
            :pid,
            :fname,
            :path,
            :ftype,
            :status
        )
        RETURNING id
        """),
        {
            "pid": patient_id,
            "fname": filename,
            "path": stored_name,
            "ftype": "PDF",
            "status": "uploaded"
        }
    )

    file_id = result.fetchone()[0]

    db.commit()
    db.close()

    print(f"✅ File uploaded: {stored_name}")
    print(f"✅ File ID: {file_id}")

    return file_id, stored_name