from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.patient import Patient
from models.profile import Profile
from schemas.auth import SignupRequest
from utils.hashing import hash_password
from datetime import datetime, timedelta

from models.otp import EmailOTP

from utils.otp import generate_otp
from utils.email import send_otp_email
from fastapi import HTTPException, status

from schemas.auth import LoginRequest, TokenResponse
from utils.hashing import verify_password
from utils.jwt import create_access_token

from schemas.auth import ForgotPasswordRequest
from schemas.auth import VerifyResetOTPRequest
from schemas.auth import ResetPasswordRequest

def signup_service(
    request: SignupRequest,
    db: Session
):
    existing_patient = (
        db.query(Patient)
        .filter(Patient.email == request.email)
        .first()
    )

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    try:
        patient = Patient(
            email=request.email,
            password_hash=hash_password(request.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(patient)
        db.flush()

        profile = Profile(
            patient_id=patient.patient_id,
            name=request.name,
            phone=request.phone,
            dob=request.dob,
            gender=request.gender
        )

        db.add(profile)

        db.commit()

        return {
            "message": "Account created successfully."
        }

    except Exception:
        db.rollback()
        raise


def login_service(
    request: LoginRequest,
    db: Session
):

    patient = (
        db.query(Patient)
        .filter(Patient.email == request.email)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(
        request.password,
        patient.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        patient_id=str(patient.patient_id),
        email=patient.email
    )

    return TokenResponse(
        access_token=access_token
    )

def forgot_password_service(
    request: ForgotPasswordRequest,
    db: Session
):

    patient = (
        db.query(Patient)
        .filter(Patient.email == request.email)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    # Invalidate any previous unused OTPs
    (
        db.query(EmailOTP)
        .filter(
            EmailOTP.patient_id == patient.patient_id,
            EmailOTP.purpose == "RESET_PASSWORD",
            EmailOTP.is_verified == False,
        )
        .update({"is_verified": True})
    )

    # Generate new OTP
    otp = generate_otp()

    otp_entry = EmailOTP(
        patient_id=patient.patient_id,
        otp_code=otp,
        purpose="RESET_PASSWORD",
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(otp_entry)
    db.commit()

    send_otp_email(
        patient.email,
        otp
    )

    return {
        "message": "OTP sent successfully."
    }

def verify_reset_otp_service(
    request: VerifyResetOTPRequest,
    db: Session
):

    patient = (
        db.query(Patient)
        .filter(Patient.email == request.email)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    otp_entry = (
        db.query(EmailOTP)
        .filter(
            EmailOTP.patient_id == patient.patient_id,
            EmailOTP.purpose == "RESET_PASSWORD",
            EmailOTP.otp_code == request.otp,
            EmailOTP.is_verified == False,
        )
        .order_by(EmailOTP.created_at.desc())
        .first()
    )

    if not otp_entry:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP."
        )

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="OTP has expired."
        )

    otp_entry.is_verified = True

    db.commit()

    return {
        "message": "OTP verified successfully."
    }

def reset_password_service(
    request: ResetPasswordRequest,
    db: Session
):

    patient = (
        db.query(Patient)
        .filter(Patient.email == request.email)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    otp_entry = (
        db.query(EmailOTP)
        .filter(
            EmailOTP.patient_id == patient.patient_id,
            EmailOTP.purpose == "RESET_PASSWORD",
            EmailOTP.otp_code == request.otp,
            EmailOTP.is_verified == True,
        )
        .order_by(EmailOTP.created_at.desc())
        .first()
    )

    if not otp_entry:
        raise HTTPException(
            status_code=400,
            detail="OTP not verified."
        )

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="OTP has expired."
        )

    patient.password_hash = hash_password(
        request.new_password
    )

    db.commit()

    return {
        "message": "Password reset successful."
    }