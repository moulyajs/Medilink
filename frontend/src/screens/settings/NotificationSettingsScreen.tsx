import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Switch,
  ScrollView,
  TouchableOpacity,
  Alert,
} from "react-native";

import {
  getNotificationSettings,
  updateNotificationSettings,
  NotificationSettings,
} from "../../services/notificationSettingsService";

export default function NotificationSettingsScreen() {
  const [settings, setSettings] =
    useState<NotificationSettings | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await getNotificationSettings();
      setSettings(data);
    } catch {
      Alert.alert("Error", "Failed to load settings.");
    }
  };

  const toggle = (key: keyof NotificationSettings) => {
    if (!settings) return;

    setSettings({
      ...settings,
      [key]: !settings[key],
    });
  };

  const save = async () => {
    if (!settings) return;

    try {
      await updateNotificationSettings(settings);

      Alert.alert(
        "Success",
        "Notification settings updated."
      );
    } catch {
      Alert.alert("Error", "Failed to save.");
    }
  };

  if (!settings) return null;

  const items = [
    {
      label: "Push Notifications",
      key: "push_notifications",
    },
    {
      label: "Email Notifications",
      key: "email_notifications",
    },
    {
      label: "Appointment Reminders",
      key: "appointment_reminders",
    },
    {
      label: "Medication Reminders",
      key: "medication_reminders",
    },
    {
      label: "Lab Report Notifications",
      key: "lab_report_notifications",
    },
    {
      label: "Health Alerts",
      key: "health_alerts",
    },
  ];

  return (
    <ScrollView style={styles.container}>
      {items.map((item) => (
        <View
          key={item.key}
          style={styles.row}
        >
          <Text style={styles.text}>
            {item.label}
          </Text>

          <Switch
            value={
              settings[
                item.key as keyof NotificationSettings
              ]
            }
            onValueChange={() =>
              toggle(
                item.key as keyof NotificationSettings
              )
            }
          />
        </View>
      ))}

      <TouchableOpacity
        style={styles.button}
        onPress={save}
      >
        <Text style={styles.buttonText}>
          Save Settings
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8FAFC",
    padding: 20,
  },

  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "white",
    padding: 18,
    borderRadius: 12,
    marginBottom: 12,
  },

  text: {
    fontSize: 16,
  },

  button: {
    marginTop: 20,
    backgroundColor: "#2563EB",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
  },

  buttonText: {
    color: "white",
    fontWeight: "700",
    fontSize: 16,
  },
});