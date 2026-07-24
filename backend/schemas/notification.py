from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class NotificationSettingsResponse(BaseModel):
    push_notifications: bool
    email_notifications: bool
    appointment_reminders: bool
    medication_reminders: bool
    lab_report_notifications: bool
    health_alerts: bool

    class Config:
        from_attributes = True


class UpdateNotificationSettingsRequest(BaseModel):
    push_notifications: bool
    email_notifications: bool
    appointment_reminders: bool
    medication_reminders: bool
    lab_report_notifications: bool
    health_alerts: bool


# -----------------------------
# Notification History
# -----------------------------

class NotificationCreate(BaseModel):
    title: str
    message: str
    notification_type: str


class NotificationResponse(BaseModel):
    notification_id: UUID
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True