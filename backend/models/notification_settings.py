from sqlalchemy import (
    Column,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.patient_id"),
        primary_key=True,
    )

    push_notifications = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    email_notifications = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    appointment_reminders = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    medication_reminders = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    lab_report_notifications = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    health_alerts = Column(
        Boolean,
        default=True,
        nullable=False,
    )