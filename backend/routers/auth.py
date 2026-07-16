from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db

from schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
)
from schemas.auth import ResetPasswordRequest
from services.auth_service import reset_password_service
from services.auth_service import (
    signup_service,
    login_service,
)
from schemas.auth import ForgotPasswordRequest
from services.auth_service import forgot_password_service
from schemas.auth import VerifyResetOTPRequest
from services.auth_service import verify_reset_otp_service
from utils.dependencies import get_current_patient
from models.patient import Patient
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db)
):
    return signup_service(request, db)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    return login_service(request, db)

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    return forgot_password_service(
        request,
        db
    )

@router.post("/verify-reset-otp")
def verify_reset_otp(
    request: VerifyResetOTPRequest,
    db: Session = Depends(get_db)
):
    return verify_reset_otp_service(
        request,
        db
    )

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    return reset_password_service(
        request,
        db
    )

@router.get("/me")
def get_logged_in_patient(
    current_patient: Patient = Depends(get_current_patient)
):
    return {
        "patient_id": str(current_patient.patient_id),
        "email": current_patient.email
    }