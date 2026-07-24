import React, { useCallback, useEffect, useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  RefreshControl,
  TouchableOpacity,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../theme/ThemeContext";

import {
  getNotifications,
  markNotificationRead,
} from "../../services/notificationService";

type Notification = {
  id: string;
  title: string;
  message: string;
  notification_type: string;
  is_read: boolean;
  created_at: string;
};

export default function NotificationScreen() {
  const { colors, darkMode } = useTheme();

  const [notifications, setNotifications] = useState<
    Notification[]
  >([]);

  const [refreshing, setRefreshing] =
    useState(false);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const data = await getNotifications();
      setNotifications(data);
    } catch (error) {
      console.log(error);
    }
  };

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    await loadNotifications();
    setRefreshing(false);
  }, []);

  const iconName = (type: string) => {
    switch (type) {
      case "anomaly":
        return "warning";

      case "trend":
        return "trending-up";

      case "report":
        return "document-text";

      default:
        return "notifications";
    }
  };

  const iconColor = (type: string) => {
    switch (type) {
      case "anomaly":
        return "#EF4444";

      case "trend":
        return "#22C55E";

      case "report":
        return "#2563EB";

      default:
        return colors.primary;
    }
  };

  const formatDate = (date: string) => {
    return new Date(date).toLocaleString();
  };

  const openNotification = async (
    notification: Notification
  ) => {
    if (!notification.is_read) {
      await markNotificationRead(notification.id);

      setNotifications((prev) =>
        prev.map((item) =>
          item.id === notification.id
            ? {
                ...item,
                is_read: true,
              }
            : item
        )
      );
    }
  };

  return (
    <SafeAreaView
      style={[
        styles.container,
        {
          backgroundColor: colors.background,
        },
      ]}
    >
      <LinearGradient
        colors={
          darkMode
            ? ["#1E293B", "#111827", "#000000"]
            : ["#5D9DFF", "#4E89B9", "#2563EB"]
        }
        style={styles.header}
      >
        <Text style={styles.headerTitle}>
          Notifications
        </Text>

        <Text style={styles.headerSubtitle}>
          Health alerts & report updates
        </Text>
      </LinearGradient>

      <ScrollView
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
          />
        }
        contentContainerStyle={styles.content}
      >
        {notifications.length === 0 ? (
          <View style={styles.empty}>
            <Ionicons
              name="notifications-off-outline"
              size={70}
              color={colors.subText}
            />

            <Text
              style={[
                styles.emptyText,
                {
                  color: colors.subText,
                },
              ]}
            >
              No Notifications Yet
            </Text>
          </View>
        ) : (
          notifications.map((item) => (
            <TouchableOpacity
              key={item.id}
              activeOpacity={0.9}
              onPress={() =>
                openNotification(item)
              }
              style={[
                styles.card,
                {
                  backgroundColor:
                    colors.card,
                  borderColor:
                    colors.border,
                },
              ]}
            >
              <View style={styles.row}>
                <View
                  style={[
                    styles.iconBox,
                    {
                      backgroundColor:
                        darkMode
                          ? "#1F2937"
                          : "#EEF6FF",
                    },
                  ]}
                >
                  <Ionicons
                    name={
                      iconName(
                        item.notification_type
                      ) as any
                    }
                    size={24}
                    color={iconColor(
                      item.notification_type
                    )}
                  />
                </View>

                <View
                  style={{ flex: 1 }}
                >
                  <Text
                    style={[
                      styles.title,
                      {
                        color:
                          colors.text,
                      },
                    ]}
                  >
                    {item.title}
                  </Text>

                  <Text
                    style={[
                      styles.message,
                      {
                        color:
                          colors.subText,
                      },
                    ]}
                  >
                    {item.message}
                  </Text>

                  <Text
                    style={[
                      styles.time,
                      {
                        color:
                          colors.subText,
                      },
                    ]}
                  >
                    {formatDate(
                      item.created_at
                    )}
                  </Text>
                </View>

                {!item.is_read && (
                  <View
                    style={
                      styles.unread
                    }
                  />
                )}
              </View>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  header: {
    paddingTop: 50,
    paddingBottom: 35,
    paddingHorizontal: 22,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },

  headerTitle: {
    color: "#FFF",
    fontSize: 28,
    fontWeight: "700",
  },

  headerSubtitle: {
    marginTop: 8,
    color: "#EAF4FF",
    fontSize: 15,
  },

  content: {
    padding: 18,
  },

  card: {
    borderRadius: 18,
    borderWidth: 1,
    padding: 16,
    marginBottom: 16,
  },

  row: {
    flexDirection: "row",
    alignItems: "center",
  },

  iconBox: {
    width: 52,
    height: 52,
    borderRadius: 15,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 15,
  },

  title: {
    fontSize: 17,
    fontWeight: "700",
  },

  message: {
    marginTop: 5,
    fontSize: 15,
    lineHeight: 22,
  },

  time: {
    marginTop: 8,
    fontSize: 12,
  },

  unread: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: "#2563EB",
    marginLeft: 10,
  },

  empty: {
    marginTop: 120,
    alignItems: "center",
  },

  emptyText: {
    marginTop: 20,
    fontSize: 18,
    fontWeight: "600",
  },
});