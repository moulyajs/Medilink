from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from database import Base


class EmailOTP(Base):
    __tablename__ = "email_otps"

    otp_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id", ondelete="CASCADE"),
        nullable=False
    )

    otp_code = Column(
        String(6),
        nullable=False
    )

    purpose = Column(
        String(30),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )