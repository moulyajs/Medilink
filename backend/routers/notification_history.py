from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

from schemas.notification_history import (
    NotificationResponse,
    CreateNotificationRequest,
)

from services.notification_history_service import (
    get_notifications_service,
    create_notification_service,
    mark_notification_read_service,
)

router = APIRouter(
    prefix="/notifications/history",
    tags=["Notification History"],
)


@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def get_notifications(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return get_notifications_service(
        current_patient,
        db,
    )


@router.post(
    "/",
    response_model=NotificationResponse,
)
def create_notification(
    request: CreateNotificationRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return create_notification_service(
        request,
        current_patient,
        db,
    )


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_read(
    notification_id: UUID,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return mark_notification_read_service(
        notification_id,
        current_patient,
        db,
    )