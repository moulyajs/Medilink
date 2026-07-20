from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from models.device import Device
from models.patient import Patient


def get_devices_service(
    current_patient: Patient,
    db: Session,
):
    devices = (
        db.query(Device)
        .filter(
            Device.patient_id == current_patient.patient_id,
            Device.active == True,
        )
        .order_by(Device.last_active.desc())
        .all()
    )

    return {
        "devices": devices
    }


def remove_device_service(
    device_id: UUID,
    current_patient: Patient,
    db: Session,
):
    device = (
        db.query(Device)
        .filter(
            Device.device_id == device_id,
            Device.patient_id == current_patient.patient_id,
            Device.active == True,
        )
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found."
        )

    device.active = False
    device.is_current = False

    db.commit()

    return {
        "message": "Device removed successfully."
    }