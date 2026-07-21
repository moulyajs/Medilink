/**
 * Dashboard.tsx
 * Medilink landing screen — greeting, quick actions, health summary,
 * latest trend, recent reports, recent alerts.
 *
 * Uses the real theme exports from src/theme/index.ts:
 *   import { Colors, Spacing, Typography } from '../../theme';
 *
 * No `radius` or `layout` file exists yet in your theme, so border
 * radii (12 for buttons/inputs, 16 for cards, per the design doc)
 * are hardcoded below. Say the word and I'll add a radius.ts export
 * so those aren't magic numbers either.
 */

import React from "react";
import { View, ScrollView, StyleSheet, TouchableOpacity } from "react-native";
import { Text, Avatar } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import {
  Upload,
  Clock,
  MessageCircle,
  TrendingUp,
  Bell,
  ChevronRight,
  FileText,
} from "lucide-react-native";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { Colors, Spacing, Typography } from "../../theme";

dayjs.extend(relativeTime);

// ---------- Types ----------

export type ReportStatus = "Normal" | "Abnormal" | "Pending";
export type ReportType = "Lab" | "ECG" | "X-Ray" | "Prescription";
export type AlertSeverity = "info" | "warning" | "critical";
export type TrendDirection = "increasing" | "stable" | "decreasing";
export type OverallStatus = "Healthy" | "Attention" | "Critical";

export interface RecentReport {
  id: string;
  title: string;
  type: ReportType;
  date: string; // ISO string
  status: ReportStatus;
}

export interface RecentAlert {
  id: string;
  message: string;
  severity: AlertSeverity;
  date: string; // ISO string
}

export interface HealthSummary {
  overallStatus: OverallStatus;
  metricsTracked: number;
  lastUpdated: string; // ISO string
}

export interface TrendPreview {
  metricName: string;
  direction: TrendDirection;
  changePercent: number;
}

interface DashboardProps {
  userName?: string;
  recentReports?: RecentReport[];
  recentAlerts?: RecentAlert[];
  healthSummary?: HealthSummary;
  latestTrend?: TrendPreview | null;
}

// ---------- Helpers ----------

const getGreeting = () => {
  const hour = dayjs().hour();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
};

const statusColor = (status: string) => {
  switch (status) {
    case "Normal":
    case "Healthy":
      return Colors.success;
    case "Abnormal":
    case "Attention":
      return Colors.warning;
    case "Critical":
    case "Pending":
      return Colors.danger;
    default:
      return Colors.textSecondary;
  }
};

const trendColor = (direction: TrendDirection) => {
  if (direction === "increasing") return Colors.success;
  if (direction === "decreasing") return Colors.warning;
  return Colors.primary;
};

const trendArrow = (direction: TrendDirection) => {
  if (direction === "increasing") return "↑";
  if (direction === "decreasing") return "↓";
  return "→";
};

const QUICK_ACTIONS = [
  { key: "upload", label: "Upload Report", icon: Upload, route: "UploadReport" },
  { key: "timeline", label: "Timeline", icon: Clock, route: "MedicalTimeline" },
  { key: "chatbot", label: "Chatbot", icon: MessageCircle, route: "ChatHome" },
  { key: "trends", label: "Trends", icon: TrendingUp, route: "TrendDashboard" },
] as const;

// Placeholder data so the screen renders something sensible even
// before it's wired to TanStack Query / Redux. Replace by passing
// real props from wherever <Dashboard /> is mounted.
const DEFAULTS: Required<Omit<DashboardProps, "latestTrend">> & {
  latestTrend: TrendPreview | null;
} = {
  userName: "there",
  recentReports: [],
  recentAlerts: [],
  healthSummary: { overallStatus: "Healthy", metricsTracked: 0, lastUpdated: dayjs().toISOString() },
  latestTrend: null,
};

// ---------- Component ----------

export default function Dashboard(props: DashboardProps) {
  const {
    userName = DEFAULTS.userName,
    recentReports = DEFAULTS.recentReports,
    recentAlerts = DEFAULTS.recentAlerts,
    healthSummary = DEFAULTS.healthSummary,
    latestTrend = DEFAULTS.latestTrend,
  } = props;

  const navigation = useNavigation<any>();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Greeting */}
      <View style={styles.greetingRow}>
        <View>
          <Text style={styles.greetingText}>{getGreeting()},</Text>
          <Text style={styles.userName}>{userName}</Text>
        </View>
        <TouchableOpacity onPress={() => navigation.navigate("Profile")}>
          <Avatar.Text
            size={48}
            label={userName.charAt(0).toUpperCase()}
            style={{ backgroundColor: Colors.primary }}
          />
        </TouchableOpacity>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActionsRow}>
        {QUICK_ACTIONS.map(({ key, label, icon: Icon, route }) => (
          <TouchableOpacity
            key={key}
            style={styles.quickAction}
            onPress={() => navigation.navigate(route)}
            activeOpacity={0.7}
          >
            <View style={styles.quickActionIconWrap}>
              <Icon size={22} color={Colors.primary} />
            </View>
            <Text style={styles.quickActionLabel}>{label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Health Summary */}
      <View style={styles.card}>
        <View style={styles.cardHeaderRow}>
          <Text style={styles.cardTitle}>Health Summary</Text>
          <View
            style={[styles.statusPill, { backgroundColor: statusColor(healthSummary.overallStatus) + "20" }]}
          >
            <Text style={[styles.statusPillText, { color: statusColor(healthSummary.overallStatus) }]}>
              {healthSummary.overallStatus}
            </Text>
          </View>
        </View>
        <Text style={styles.cardSubtext}>
          {healthSummary.metricsTracked} metrics tracked · updated {dayjs(healthSummary.lastUpdated).fromNow()}
        </Text>
      </View>

      {/* Latest Trend */}
      {latestTrend && (
        <TouchableOpacity
          style={styles.card}
          onPress={() => navigation.navigate("TrendDashboard")}
          activeOpacity={0.8}
        >
          <View style={styles.cardHeaderRow}>
            <Text style={styles.cardTitle}>Latest Trend</Text>
            <ChevronRight size={18} color={Colors.textSecondary} />
          </View>
          <View style={styles.trendRow}>
            <Text style={styles.trendMetric}>{latestTrend.metricName}</Text>
            <Text style={[styles.trendValue, { color: trendColor(latestTrend.direction) }]}>
              {trendArrow(latestTrend.direction)} {Math.abs(latestTrend.changePercent)}%
            </Text>
          </View>
        </TouchableOpacity>
      )}

      {/* Recent Reports */}
      <View style={styles.sectionHeaderRow}>
        <Text style={styles.sectionTitle}>Recent Reports</Text>
        <TouchableOpacity onPress={() => navigation.navigate("ReportsList")}>
          <Text style={styles.seeAll}>See all</Text>
        </TouchableOpacity>
      </View>
      {recentReports.length === 0 ? (
        <View style={styles.card}>
          <Text style={styles.emptyText}>No reports uploaded yet</Text>
        </View>
      ) : (
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalList}>
          {recentReports.map((report) => (
            <TouchableOpacity
              key={report.id}
              style={styles.reportCard}
              onPress={() => navigation.navigate("ReportDetails", { reportId: report.id })}
              activeOpacity={0.8}
            >
              <FileText size={20} color={Colors.primary} />
              <Text style={styles.reportCardTitle} numberOfLines={1}>
                {report.title}
              </Text>
              <Text style={styles.reportCardType}>{report.type}</Text>
              <Text style={styles.reportCardDate}>{dayjs(report.date).format("DD MMM YYYY")}</Text>
              <View style={[styles.statusPillSmall, { backgroundColor: statusColor(report.status) + "20" }]}>
                <Text style={[styles.statusPillTextSmall, { color: statusColor(report.status) }]}>
                  {report.status}
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}

      {/* Recent Alerts */}
      <View style={styles.sectionHeaderRow}>
        <Text style={styles.sectionTitle}>Recent Alerts</Text>
        <TouchableOpacity onPress={() => navigation.navigate("Notifications")}>
          <Text style={styles.seeAll}>See all</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.card}>
        {recentAlerts.length === 0 && <Text style={styles.emptyText}>No new alerts</Text>}
        {recentAlerts.map((alert, index) => (
          <View key={alert.id} style={[styles.alertRow, index < recentAlerts.length - 1 && styles.alertRowBorder]}>
            <Bell
              size={18}
              color={
                alert.severity === "critical"
                  ? Colors.danger
                  : alert.severity === "warning"
                  ? Colors.warning
                  : Colors.primary
              }
            />
            <View style={styles.alertTextWrap}>
              <Text style={styles.alertMessage}>{alert.message}</Text>
              <Text style={styles.alertDate}>{dayjs(alert.date).fromNow()}</Text>
            </View>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

// ---------- Styles ----------

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: Spacing.md, paddingBottom: Spacing.xxxl },
  greetingRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: Spacing.lg,
  },
  greetingText: { ...Typography.small, color: Colors.textSecondary },
  userName: { ...Typography.sectionTitle, color: Colors.text },
  quickActionsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: Spacing.lg,
  },
  quickAction: { alignItems: "center", flex: 1 },
  quickActionIconWrap: {
    width: 52,
    height: 52,
    borderRadius: 16,
    backgroundColor: Colors.background,
    borderWidth: 1,
    borderColor: Colors.border,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: Spacing.xs,
  },
  quickActionLabel: { ...Typography.caption, color: Colors.textSecondary, textAlign: "center" },
  card: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    padding: Spacing.md,
    marginBottom: Spacing.md,
    borderWidth: 1,
    borderColor: Colors.border,
    shadowColor: Colors.shadow,
    shadowOpacity: 0.04,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 1,
  },
  cardHeaderRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  cardTitle: { ...Typography.cardTitle, color: Colors.text },
  cardSubtext: { ...Typography.small, color: Colors.textSecondary, marginTop: Spacing.xs },
  statusPill: { paddingHorizontal: Spacing.sm, paddingVertical: 4, borderRadius: 20 },
  statusPillText: { ...Typography.caption, fontWeight: "600" as const },
  statusPillSmall: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 2,
    borderRadius: 20,
    alignSelf: "flex-start",
    marginTop: Spacing.xs,
  },
  statusPillTextSmall: { fontSize: 11, fontWeight: "600" as const },
  trendRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: Spacing.sm },
  trendMetric: { ...Typography.body, color: Colors.text },
  trendValue: { ...Typography.cardTitle },
  sectionHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: Spacing.sm,
  },
  sectionTitle: { ...Typography.sectionTitle, fontSize: 18, color: Colors.text },
  seeAll: { ...Typography.small, color: Colors.primary, fontWeight: "500" as const },
  horizontalList: { marginBottom: Spacing.lg },
  reportCard: {
    width: 140,
    backgroundColor: Colors.background,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.sm,
    marginRight: Spacing.sm,
  },
  reportCardTitle: { ...Typography.small, fontWeight: "600" as const, color: Colors.text, marginTop: Spacing.xs },
  reportCardType: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  reportCardDate: { fontSize: 11, color: Colors.textSecondary, marginTop: 2 },
  alertRow: { flexDirection: "row", alignItems: "flex-start", paddingVertical: Spacing.sm },
  alertRowBorder: { borderBottomWidth: 1, borderBottomColor: Colors.border },
  alertTextWrap: { marginLeft: Spacing.sm, flex: 1 },
  alertMessage: { ...Typography.body, color: Colors.text },
  alertDate: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  emptyText: { ...Typography.small, color: Colors.textSecondary, paddingVertical: Spacing.sm },
});
