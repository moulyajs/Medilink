from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.patient import Patient
from utils.dependencies import get_current_patient

from schemas.notification import (
    NotificationSettingsResponse,
    UpdateNotificationSettingsRequest,
)

from services.notification_service import (
    get_notification_settings_service,
    update_notification_settings_service,
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