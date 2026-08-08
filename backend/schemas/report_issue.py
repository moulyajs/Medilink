from pydantic import BaseModel, EmailStr, Field


class ReportIssueRequest(BaseModel):

    email: EmailStr

    category: str = Field(..., min_length=3)

    title: str = Field(..., min_length=3)

    description: str = Field(..., min_length=10)


class ReportIssueResponse(BaseModel):

    message: str