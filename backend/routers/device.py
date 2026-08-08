from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

from services.device_service import (
    get_devices_service,
    remove_device_service,
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get("/")
def get_devices(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return get_devices_service(
        current_patient,
        db,
    )


@router.delete("/{device_id}")
def remove_device(
    device_id: UUID,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    print(f"Deleting device: {device_id}")

    return remove_device_service(
        device_id,
        current_patient,
        db,
    )