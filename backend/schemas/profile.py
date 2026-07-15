from datetime import date
from uuid import UUID

from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str

    phone: str | None = None

    dob: date | None = None

    gender: str | None = None

    blood_group: str | None = None

    address: str | None = None

    emergency_contact: str | None = None

    profile_image: str | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    patient_id: UUID

    class Config:
        from_attributes = True