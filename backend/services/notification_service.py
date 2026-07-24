from sqlalchemy.orm import Session

from models.notification_settings import NotificationSettings
from models.patient import Patient
from schemas.notification import UpdateNotificationSettingsRequest
from models.notification import Notification

from schemas.notification import (
    NotificationCreate,
)

def get_notification_settings_service(
    current_patient: Patient,
    db: Session,
):
    settings = (
        db.query(NotificationSettings)
        .filter(
            NotificationSettings.patient_id == current_patient.patient_id
        )
        .first()
    )

    if not settings:
        settings = NotificationSettings(
            patient_id=current_patient.patient_id
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


def update_notification_settings_service(
    request: UpdateNotificationSettingsRequest,
    current_patient: Patient,
    db: Session,
):
    settings = (
        db.query(NotificationSettings)
        .filter(
            NotificationSettings.patient_id == current_patient.patient_id
        )
        .first()
    )

    if not settings:
        settings = NotificationSettings(
            patient_id=current_patient.patient_id
        )
        db.add(settings)

    settings.push_notifications = request.push_notifications
    settings.email_notifications = request.email_notifications
    settings.appointment_reminders = request.appointment_reminders
    settings.medication_reminders = request.medication_reminders
    settings.lab_report_notifications = request.lab_report_notifications
    settings.health_alerts = request.health_alerts

    db.commit()
    db.refresh(settings)

    return settings

# ----------------------------------------
# Notification History
# ----------------------------------------

def create_notification_service(
    request: NotificationCreate,
    current_patient: Patient,
    db: Session,
):
    notification = Notification(
        patient_id=current_patient.patient_id,
        title=request.title,
        message=request.message,
        notification_type=request.notification_type,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_notifications_service(
    current_patient: Patient,
    db: Session,
):
    return (
        db.query(Notification)
        .filter(
            Notification.patient_id ==
            current_patient.patient_id
        )
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )


def mark_notification_read_service(
    notification_id,
    current_patient: Patient,
    db: Session,
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.notification_id == notification_id,
            Notification.patient_id == current_patient.patient_id,
        )
        .first()
    )

    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)

    return notification