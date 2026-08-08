from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

from schemas.notification import (
    NotificationSettingsResponse,
    UpdateNotificationSettingsRequest,
    NotificationResponse,
    NotificationCreate,
)

from services.notification_service import (
    get_notification_settings_service,
    update_notification_settings_service,
    create_notification_service,
    get_notifications_service,
    mark_notification_read_service,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "/",
    response_model=NotificationSettingsResponse,
)
def get_notification_settings(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return get_notification_settings_service(
        current_patient,
        db,
    )


@router.put(
    "/",
    response_model=NotificationSettingsResponse,
)
def update_notification_settings(
    request: UpdateNotificationSettingsRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return update_notification_settings_service(
        request,
        current_patient,
        db,
    )

# --------------------------------------------------
# Notification History
# --------------------------------------------------

@router.get(
    "/history",
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
    "/create",
    response_model=NotificationResponse,
)
def create_notification(
    request: NotificationCreate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return create_notification_service(
        request,
        current_patient,
        db,
    )


@router.put(
    "/read/{notification_id}",
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