from fastapi import FastAPI, UploadFile, File, HTTPException
from storage import client, BUCKET
from database import SessionLocal
import uuid
import io
from sqlalchemy import text
from fastapi.responses import StreamingResponse
app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    try:
        # Generate unique ID
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"

        # Read file as bytes
        content = await file.read()

        # Convert bytes to stream (IMPORTANT)
        file_stream = io.BytesIO(content)

        # Upload to MinIO (FIXED)
        client.put_object(
            BUCKET,
            filename,
            file_stream,
            length=len(content),
            content_type=file.content_type
        )

        # Save metadata in DB
        db = SessionLocal()

        db.execute(
        text("""
        INSERT INTO files (file_name, file_path, file_type, status)
        VALUES (:name, :path, :type, :status)
        """),
    {
        "name": file.filename,
        "path": filename,
        "type": file.content_type,
        "status": "uploaded"
    }
)

        db.commit()
        db.close()

        return {
            "status": "success",
            "file_id": file_id,
            "filename": filename
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/")
def get_files():

    db = SessionLocal()

    result = db.execute(
        text("SELECT id, file_name, file_path, upload_date, status FROM files")
    )

    files = []

    for row in result:
        files.append({
            "id": row.id,
            "file_name": row.file_name,
            "file_path": row.file_path,
            "upload_date": str(row.upload_date),
            "status": row.status
        })

    db.close()

    return files

@app.get("/view/{file_path}")
def view_file(file_path: str):

    try:
        obj = client.get_object(BUCKET, file_path)

        return StreamingResponse(
            obj,
            media_type="application/pdf"  # works for PDFs
        )

    except:
        raise HTTPException(status_code=404)
