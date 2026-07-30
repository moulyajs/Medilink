/**
 * Dashboard.tsx
 * Medilink Dashboard
 */

import React, {
  useEffect,
  useState,
} from "react";

import {
  View,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
} from "react-native";

import {
  Text,
  Avatar,
  ActivityIndicator,
} from "react-native-paper";

import {
  useNavigation,
} from "@react-navigation/native";

import { Ionicons } from "@expo/vector-icons";

import {
  getNotifications,
} from "../../services/notificationService";

import {
  Upload,
  Clock,
  MessageCircle,
  TrendingUp,
  Bell,
  ChevronRight,
  FileText,
  AlertTriangle,
} from "lucide-react-native";

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

import {
  Colors,
  Spacing,
  Typography,
} from "../../theme";

import {
  getReports,
  ReportListItem,
} from "../../services/reportService";

import { getProfile, Profile } from "../../services/profileService";


dayjs.extend(relativeTime);

const getGreeting = () => {
  const hour = dayjs().hour();

  if (hour < 12)
    return "Good morning";

  if (hour < 17)
    return "Good afternoon";

  return "Good evening";
};

const statusColor = (
  status: string
) => {
  switch (status) {
    case "Healthy":
    case "Normal":
      return Colors.success;

    case "Abnormal":
    case "Attention":
      return Colors.warning;

    case "Pending":
    case "Critical":
      return Colors.danger;

    default:
      return Colors.textSecondary;
  }
};

const QUICK_ACTIONS = [
  {
    label: "Upload",
    icon: Upload,
    route: "UploadReport",
  },
  {
    label: "Timeline",
    icon: Clock,
    route: "MedicalTimeline",
  },
  {
    label: "Chat",
    icon: MessageCircle,
    route: "ChatHome",
  },
  {
    label: "Trends",
    icon: TrendingUp,
    route: "Trend",
  },
  {
    label: "Anomalies",
    icon: AlertTriangle,
    route: "Anomaly",
  },
];

export default function Dashboard() {

  const navigation =
    useNavigation<any>();

  const [loading,
    setLoading] =
    useState(true);

  const [profile, 
    setProfile] = 
    useState<Profile | null>(null);

  const [reports,
    setReports] =
    useState<
      ReportListItem[]
    >([]);
    const [unreadCount, setUnreadCount] =
  useState(0);
  useEffect(() => {
  loadReports();
  loadUnreadCount();
  loadProfile();
}, []);


const loadUnreadCount = async () => {
  try {
    const notifications = await getNotifications();

    const unread = notifications.filter(
      (item: any) => !item.is_read
    );

    setUnreadCount(unread.length);
  } catch (err) {
    console.log(err);
  }
};

  const loadReports =
    async () => {
      try {
        setLoading(true);

        const data =
          await getReports();

        console.log(
          "Dashboard Reports",
          data
        );

        setReports(data);

      } catch (error) {
        console.error(
          error
        );
      } finally {
        setLoading(false);
      }
    };

    const loadProfile = async () => {
      try {
        const data = await getProfile();
        setProfile(data);
      } catch (error) {
        console.log("Profile Error:", error);
      }
    };

  const totalReports =
    reports.length;

  const abnormalReports =
    reports.filter(
      report =>
        report.status ===
        "Abnormal"
    ).length;

  const pendingReports =
    reports.filter(
      report =>
        report.status ===
        "Pending"
    ).length;

  const latestUpload =
    reports.length > 0
      ? reports[0]
          .upload_date
      : dayjs()
          .toISOString();

  const overallStatus =
    abnormalReports > 0
      ? "Attention"
      : pendingReports > 0
      ? "Critical"
      : "Healthy";

  const recentReports =
    reports.slice(0, 5);

  if (loading) {
    return (
      <View
        style={{
          flex: 1,
          justifyContent:
            "center",
          alignItems:
            "center",
        }}
      >
        <ActivityIndicator
          size="large"
        />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={
        styles.content
      }
    >
      <View
        style={
          styles.greetingRow
        }
      >
        <View>
          <Text
            style={
              styles.greetingText
            }
          >
            {getGreeting()},
          </Text>

          <Text
            style={
              styles.userName
            }
          >
            {profile?.name ?? "User"}
          </Text>
        </View>

        <View
  style={{
    flexDirection: "row",
    alignItems: "center",
  }}
>
  <TouchableOpacity
    onPress={() =>
      navigation.navigate(
        "Notifications"
      )
    }
    style={{
      marginRight: 16,
    }}
  >
    <View>
      <Ionicons
        name="notifications"
        size={28}
        color={Colors.primary}
      />

      {unreadCount > 0 && (
        <View
          style={styles.badge}
        >
          <Text
            style={styles.badgeText}
          >
            {unreadCount}
          </Text>
        </View>
      )}
    </View>
  </TouchableOpacity>

  <TouchableOpacity
    onPress={() =>
      navigation.navigate(
        "Profile"
      )
    }
  >
    <Avatar.Text
      size={48}
      label={profile?.name?.charAt(0).toUpperCase() ?? "U"}
      style={{
        backgroundColor:
          Colors.primary,
      }}
    />
  </TouchableOpacity>
</View>
      </View>

      <View
        style={
          styles.quickActionsRow
        }
      >        {QUICK_ACTIONS.map(
          ({
            label,
            icon: Icon,
            route,
          }) => (
            <TouchableOpacity
              key={label}
              style={
                styles.quickAction
              }
              activeOpacity={0.8}
              onPress={() =>
                navigation.navigate(
                  route
                )
              }
            >
              <View
                style={
                  styles.quickActionIconWrap
                }
              >
                <Icon
                  size={22}
                  color={
                    Colors.primary
                  }
                />
              </View>

              <Text
                style={
                  styles.quickActionLabel
                }
              >
                {label}
              </Text>
            </TouchableOpacity>
          )
        )}
      </View>

      <View style={styles.card}>
        <View
          style={
            styles.cardHeaderRow
          }
        >
          <Text
            style={
              styles.cardTitle
            }
          >
            Health Summary
          </Text>

          <View
            style={[
              styles.statusPill,
              {
                backgroundColor:
                  statusColor(
                    overallStatus
                  ) + "20",
              },
            ]}
          >
            <Text
              style={[
                styles.statusPillText,
                {
                  color:
                    statusColor(
                      overallStatus
                    ),
                },
              ]}
            >
              {overallStatus}
            </Text>
          </View>
        </View>

        <Text
          style={
            styles.cardSubtext
          }
        >
          {totalReports} reports uploaded
        </Text>

        <Text
          style={
            styles.cardSubtext
          }
        >
          {abnormalReports}
          {" "}
          abnormal reports
        </Text>

        <Text
          style={
            styles.cardSubtext
          }
        >
          Updated{" "}
          {dayjs(
            latestUpload
          ).fromNow()}
        </Text>
      </View>

      <View
        style={
          styles.sectionHeaderRow
        }
      >
        <Text
          style={
            styles.sectionTitle
          }
        >
          Recent Reports
        </Text>

        <TouchableOpacity
          onPress={() =>
            navigation.navigate(
              "ReportsList"
            )
          }
        >
          <Text
            style={
              styles.seeAll
            }
          >
            See all
          </Text>
        </TouchableOpacity>
      </View>      {recentReports.length === 0 ? (
        <View style={styles.card}>
          <Text style={styles.emptyText}>
            No reports uploaded yet
          </Text>
        </View>
      ) : (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.horizontalList}
        >
          {recentReports.map(
            (report) => (
              <TouchableOpacity
                key={
                  report.document_id
                }
                style={
                  styles.reportCard
                }
                activeOpacity={
                  0.8
                }
                onPress={() =>
                  navigation.navigate(
                    "ReportDetails",
                    {
                      documentId:
                        report.document_id,
                    }
                  )
                }
              >
                <FileText
                  size={22}
                  color={
                    Colors.primary
                  }
                />

                <Text
                  style={
                    styles.reportCardTitle
                  }
                  numberOfLines={1}
                >
                  {report.document_type
                    .replace(
                      /_/g,
                      " "
                    )
                    .replace(
                      /\b\w/g,
                      c =>
                        c.toUpperCase()
                    )}
                </Text>

                <Text
                  style={
                    styles.reportCardDate
                  }
                >
                  {dayjs(
                    report.upload_date
                  ).format(
                    "DD MMM YYYY"
                  )}
                </Text>

                <View
                  style={[
                    styles.statusPillSmall,
                    {
                      backgroundColor:
                        statusColor(
                          report.status
                        ) +
                        "20",
                    },
                  ]}
                >
                  <Text
                    style={[
                      styles.statusPillTextSmall,
                      {
                        color:
                          statusColor(
                            report.status
                          ),
                      },
                    ]}
                  >
                    {report.status}
                  </Text>
                </View>
              </TouchableOpacity>
            )
          )}
        </ScrollView>
      )}

      <View
        style={
          styles.sectionHeaderRow
        }
      >
        <Text
          style={
            styles.sectionTitle
          }
        >
          Recent Alerts
        </Text>
      </View>

      <View
        style={styles.card}
      >
        {abnormalReports >
        0 ? (
          <View
            style={
              styles.alertRow
            }
          >
            <Bell
              size={18}
              color={
                Colors.warning
              }
            />

            <View
              style={
                styles.alertTextWrap
              }
            >
              <Text
                style={
                  styles.alertMessage
                }
              >
                {
                  abnormalReports
                }{" "}
                abnormal
                report
                {abnormalReports >
                1
                  ? "s"
                  : ""}{" "}
                detected.
              </Text>

              <Text
                style={
                  styles.alertDate
                }
              >
                Review
                these
                reports.
              </Text>
            </View>
          </View>
        ) : (
          <Text
            style={
              styles.emptyText
            }
          >
            No new alerts
          </Text>
        )}
      </View>
    </ScrollView>
  );
}const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },

  content: {
    padding: Spacing.md,
    paddingBottom: Spacing.xxxl,
  },

  greetingRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: Spacing.lg,
  },

  greetingText: {
    ...Typography.small,
    color: Colors.textSecondary,
  },

  userName: {
    ...Typography.sectionTitle,
    color: Colors.text,
  },

  quickActionsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: Spacing.lg,
  },

  quickAction: {
    alignItems: "center",
    flex: 1,
  },

  quickActionIconWrap: {
    width: 52,
    height: 52,
    borderRadius: 16,
    backgroundColor: Colors.background,
    borderWidth: 1,
    borderColor: Colors.border,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: Spacing.xs,
  },

  quickActionLabel: {
    ...Typography.caption,
    color: Colors.textSecondary,
    textAlign: "center",
  },

  card: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    marginBottom: Spacing.md,
    shadowColor: Colors.shadow,
    shadowOpacity: 0.05,
    shadowRadius: 6,
    shadowOffset: {
      width: 0,
      height: 2,
    },
    elevation: 2,
  },

  cardHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  cardTitle: {
    ...Typography.cardTitle,
    color: Colors.text,
  },

  cardSubtext: {
    ...Typography.small,
    color: Colors.textSecondary,
    marginTop: Spacing.xs,
  },

  statusPill: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: 20,
  },

  statusPillText: {
    ...Typography.caption,
    fontWeight: "600",
  },

  statusPillSmall: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 3,
    borderRadius: 20,
    alignSelf: "flex-start",
    marginTop: Spacing.sm,
  },

  statusPillTextSmall: {
    fontSize: 11,
    fontWeight: "600",
  },

  sectionHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: Spacing.sm,
  },

  sectionTitle: {
    ...Typography.sectionTitle,
    color: Colors.text,
    fontSize: 18,
  },

  seeAll: {
    ...Typography.small,
    color: Colors.primary,
    fontWeight: "600",
  },

  horizontalList: {
    marginBottom: Spacing.lg,
  },

  reportCard: {
    width: 150,
    backgroundColor: Colors.background,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.sm,
    marginRight: Spacing.sm,
  },

  reportCardTitle: {
    ...Typography.small,
    color: Colors.text,
    fontWeight: "600",
    marginTop: Spacing.sm,
  },

  reportCardDate: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 4,
  },

  alertRow: {
    flexDirection: "row",
    alignItems: "flex-start",
  },

  alertTextWrap: {
    marginLeft: Spacing.sm,
    flex: 1,
  },

  alertMessage: {
    ...Typography.body,
    color: Colors.text,
  },

  alertDate: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 2,
  },

  emptyText: {
    ...Typography.small,
    color: Colors.textSecondary,
    textAlign: "center",
    paddingVertical: Spacing.md,
  },
  badge: {
  position: "absolute",
  top: -5,
  right: -6,
  width: 18,
  height: 18,
  borderRadius: 9,
  backgroundColor: "#EF4444",
  justifyContent: "center",
  alignItems: "center",
},

badgeText: {
  color: "#FFFFFF",
  fontSize: 10,
  fontWeight: "700",
},
});