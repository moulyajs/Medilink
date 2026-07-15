from pydantic import BaseModel, EmailStr, Field


# ----------------------------
# Signup
# ----------------------------
class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(..., min_length=8)

    phone: str | None = None

    dob: str | None = None

    gender: str | None = None


# ----------------------------
# Verify Email OTP
# ----------------------------
class VerifyOTPRequest(BaseModel):
    email: EmailStr

    otp: str = Field(..., min_length=6, max_length=6)


# ----------------------------
# Login
# ----------------------------
class LoginRequest(BaseModel):
    email: EmailStr

    password: str


# ----------------------------
# Forgot Password
# ----------------------------
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# ----------------------------
# Reset Password
# ----------------------------
class ResetPasswordRequest(BaseModel):
    email: EmailStr

    otp: str

    new_password: str = Field(..., min_length=8)


# ----------------------------
# JWT Response
# ----------------------------
class TokenResponse(BaseModel):
    access_token: str

    token_type: str = "bearer"

from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)

