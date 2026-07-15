from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.profile import Profile
from models.patient import Patient
from schemas.profile import ProfileUpdate


def get_profile_service(
    current_patient: Patient,
    db: Session
):
    profile = (
        db.query(Profile)
        .filter(
            Profile.patient_id == current_patient.patient_id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    return profile


def update_profile_service(
    current_patient: Patient,
    request: ProfileUpdate,
    db: Session
):
    profile = (
        db.query(Profile)
        .filter(
            Profile.patient_id == current_patient.patient_id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return profile