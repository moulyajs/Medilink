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
        document_id (UUID)
        stored_name (str)
    """

    # Generate unique filename
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
        length=len(content),
    )

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                INSERT INTO documents
                (
                    patient_id,
                    document_type,
                    upload_date,
                    file_path
                )
                VALUES
                (
                    :patient_id,
                    :document_type,
                    NOW(),
                    :file_path
                )
                RETURNING document_id
            """),
            {
                "patient_id": patient_id,
                "document_type": "LAB_REPORT",
                "file_path": stored_name,
            },
        )

        document_id = result.fetchone()[0]

        db.commit()

        print(f"✅ File uploaded: {stored_name}")
        print(f"✅ Document ID: {document_id}")

        return document_id, stored_name

    finally:
        db.close()