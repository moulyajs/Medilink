from pydantic import BaseModel, EmailStr, Field


class ContactSupportRequest(BaseModel):
    email: EmailStr
    subject: str = Field(..., min_length=3, max_length=100)
    message: str = Field(..., min_length=10)


class ContactSupportResponse(BaseModel):
    message: str