from sqlalchemy.orm import Session

from models.notification import Notification
from models.patient import Patient

from schemas.notification_history import (
    CreateNotificationRequest,
)


def get_notifications_service(
    current_patient: Patient,
    db: Session,
):
    return (
        db.query(Notification)
        .filter(
            Notification.patient_id
            == current_patient.patient_id
        )
        .order_by(Notification.created_at.desc())
        .all()
    )


def create_notification_service(
    request: CreateNotificationRequest,
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


def mark_notification_read_service(
    notification_id,
    current_patient: Patient,
    db: Session,
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.notification_id
            == notification_id,
            Notification.patient_id
            == current_patient.patient_id,
        )
        .first()
    )

    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)

    return notification