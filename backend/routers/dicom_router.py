import base64
import io
import uuid
import numpy as np
import pydicom

from sqlalchemy import text
from storage import client, BUCKET
from database import SessionLocal
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image
from pydicom.errors import InvalidDicomError

from scripts.dicom_viewer import (
    normalize_image,
    extract_dicom_metadata,
)

router = APIRouter(
    prefix="/dicom",
    tags=["DICOM Viewer"],
)
from fastapi import Depends
from utils.dependencies import get_current_patient
from models.patient import Patient
@router.post("/view")
async def view_dicom(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    contents = await file.read()

    try:
        ds = pydicom.dcmread(
            io.BytesIO(contents),
            force=False,
        )

        if "PixelData" not in ds:
            raise HTTPException(
                status_code=400,
                detail="DICOM file contains no pixel data.",
            )

        img = ds.pixel_array

        if img.ndim == 3:
            # Select the middle slice of a 3D volume.
            img = img[img.shape[0] // 2]

        elif img.ndim != 2:
            raise HTTPException(
                status_code=400,
                detail="Unsupported DICOM image dimensions.",
            )

        img_display = normalize_image(img)

        # Convert the image to PNG in memory.
        image_buffer = io.BytesIO()

        Image.fromarray(img_display).save(
            image_buffer,
            format="PNG",
        )

        image_base64 = base64.b64encode(
            image_buffer.getvalue()
        ).decode("utf-8")

        metadata = extract_dicom_metadata(ds)

        # Convert NumPy or other non-JSON values.
        metadata = {
            key: (
                value.item()
                if isinstance(value, np.generic)
                else str(value)
                if not isinstance(
                    value, (str, int, float, bool, type(None))
                )
                else value
            )
            for key, value in metadata.items()
        }

        return {
            "success": True,
            "image": f"data:image/png;base64,{image_base64}",
            "metadata": metadata,
        }

    except HTTPException:
        raise

    except (InvalidDicomError, ValueError, OSError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read DICOM file: {str(exc)}",
        )

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Unable to process this DICOM image.",
        )

    finally:
        await file.close()
    
@router.post("/save")
async def save_dicom(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # Validate that the file is a readable DICOM image.
    try:
        ds = pydicom.dcmread(
            io.BytesIO(contents),
            force=False,
        )

        if "PixelData" not in ds:
            raise HTTPException(
                status_code=400,
                detail="The DICOM file contains no pixel data.",
            )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unreadable DICOM file.",
        )

    # Generate a unique storage filename.
    file_id = str(uuid.uuid4())
    stored_filename = f"{file_id}.dcm"

    db = SessionLocal()

    try:
        # Save the original DICOM file to MinIO.
        client.put_object(
            BUCKET,
            stored_filename,
            io.BytesIO(contents),
            length=len(contents),
            content_type="application/dicom",
        )

        # Associate the file with the authenticated patient.
        db.execute(
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
                    :pid,
                    :dtype,
                    NOW(),
                    :path
                )
            """),
            {
                "pid": str(current_patient.patient_id),
                "dtype": "application/dicom",
                "path": stored_filename,
            },
        )

        db.commit()

        return {
            "success": True,
            "message": "DICOM scan saved successfully.",
            "file_name": stored_filename,
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save the DICOM scan.",
        )

    finally:
        db.close()
        await file.close()
