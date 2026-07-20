from pydantic import BaseModel


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