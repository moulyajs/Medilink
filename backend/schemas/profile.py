from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    gender: str
    blood_group: str

    dob: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    profile_image: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int

    class Config:
        from_attributes = True