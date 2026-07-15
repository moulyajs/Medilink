from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.profile import Profile
from schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


# -----------------------------
# Create Profile
# -----------------------------
@router.post("/", response_model=ProfileResponse)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Profile)
        .filter(Profile.email == profile.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists."
        )

    new_profile = Profile(**profile.model_dump())

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# -----------------------------
# Get Profile
# -----------------------------
@router.get(
    "/{profile_id}",
    response_model=ProfileResponse
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(Profile)
        .filter(Profile.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    return profile


# -----------------------------
# Update Profile
# -----------------------------
@router.put(
    "/{profile_id}",
    response_model=ProfileResponse
)
def update_profile(
    profile_id: int,
    updated: ProfileUpdate,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(Profile)
        .filter(Profile.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    for key, value in updated.model_dump().items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return profile


# -----------------------------
# Delete Profile
# -----------------------------
@router.delete("/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(Profile)
        .filter(Profile.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found."
        )

    db.delete(profile)
    db.commit()

    return {
        "message": "Profile deleted successfully."
    }