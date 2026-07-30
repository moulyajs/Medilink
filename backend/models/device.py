from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from database import Base


class Device(Base):
    __tablename__ = "devices"

    device_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id"),
        nullable=False,
    )
    session_id = Column(
    UUID(as_uuid=True),
    unique=True,
    nullable=False,
    default=uuid.uuid4,
    )

    device_name = Column(
        String,
        nullable=False,
    )

    device_type = Column(
        String,
        nullable=False,
    )

    device_os = Column(
        String,
        nullable=False,
    )
    expo_push_token = Column(
    String,
    nullable=True,
    )
    last_active = Column(
        DateTime,
        default=datetime.utcnow,
    )

    is_current = Column(
        Boolean,
        default=False,
    )
    active = Column(
    Boolean,
    default=True,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )