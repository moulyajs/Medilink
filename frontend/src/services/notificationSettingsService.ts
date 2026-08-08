import api from "./api";

export interface NotificationSettings {
  push_notifications: boolean;
  email_notifications: boolean;
  appointment_reminders: boolean;
  medication_reminders: boolean;
  lab_report_notifications: boolean;
  health_alerts: boolean;
}

export async function getNotificationSettings() {
  const response = await api.get(
    "/notifications"
  );

  return response.data;
}

export async function updateNotificationSettings(
  settings: NotificationSettings
) {
  const response = await api.put(
    "/notifications",
    settings
  );

  return response.data;
}