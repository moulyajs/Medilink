import api from "./api";

export interface Notification {
  notification_id: string;
  title: string;
  message: string;
  notification_type: string;
  is_read: boolean;
  created_at: string;
}

export interface NotificationSettings {
  push_notifications: boolean;
  email_notifications: boolean;
  appointment_reminders: boolean;
  medication_reminders: boolean;
  lab_report_notifications: boolean;
  health_alerts: boolean;
}

/* ---------- Notification History ---------- */

export async function getNotifications() {
  const response = await api.get(
    "/notifications/history/"
  );

  return response.data;
}

export async function markNotificationRead(
  notificationId: string
) {
  const response = await api.put(
    `/notifications/history/${notificationId}/read`
  );

  return response.data;
}

export async function createNotification(
  title: string,
  message: string,
  notificationType: string
) {
  const response = await api.post(
    "/notifications/history/",
    {
      title,
      message,
      notification_type: notificationType,
    }
  );

  return response.data;
}

/* ---------- Notification Settings ---------- */

export async function getNotificationSettings() {
  const response = await api.get(
    "/notifications/"
  );

  return response.data;
}

export async function updateNotificationSettings(
  settings: NotificationSettings
) {
  const response = await api.put(
    "/notifications/",
    settings
  );

  return response.data;
}