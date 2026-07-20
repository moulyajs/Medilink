from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from models.patient import Patient

from schemas.profile import (
    ProfileResponse,
    ProfileUpdate
)

from services.profile_service import (
    get_profile_service,
    update_profile_service
)

from utils.dependencies import get_current_patient

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get(
    "/me",
    response_model=ProfileResponse
)
def get_profile(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    return get_profile_service(
        current_patient,
        db
    )


@router.put(
    "/me",
    response_model=ProfileResponse
)
def update_profile(
    request: ProfileUpdate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    return update_profile_service(
        current_patient,
        request,
        db
    )