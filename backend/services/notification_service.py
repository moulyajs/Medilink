from sqlalchemy.orm import Session

from models.notification_settings import NotificationSettings
from models.patient import Patient
from schemas.notification import UpdateNotificationSettingsRequest


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