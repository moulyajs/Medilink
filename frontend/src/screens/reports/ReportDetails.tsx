/**
 * ReportDetails.tsx
 * Shows a single report's lab values against reference ranges, with
 * per-value normal/abnormal flags, plus "View Trend" and "Ask AI"
 * actions.
 *
 * Expected route param: { reportId: string } (from ReportsList or
 * Dashboard navigation calls).
 *
 * Uses the real theme exports from src/theme/index.ts:
 *   import { Colors, Spacing, Typography } from '../../theme';
 */

import React from "react";
import { View, ScrollView, StyleSheet, TouchableOpacity } from "react-native";
import { Text } from "react-native-paper";
import { useNavigation, useRoute } from "@react-navigation/native";
import { TrendingUp, Sparkles, ChevronLeft, AlertTriangle } from "lucide-react-native";
import dayjs from "dayjs";
import { Colors, Spacing, Typography } from "../../theme";

// ---------- Types ----------

export type ReportType = "Lab" | "ECG" | "X-Ray" | "Prescription";
export type ValueFlag = "Normal" | "Abnormal";

export interface LabValue {
  id: string;
  testName: string; // e.g. "Hemoglobin"
  value: number;
  unit: string; // e.g. "g/dL"
  referenceLow: number;
  referenceHigh: number;
  flag: ValueFlag;
}

export interface ReportDetailsData {
  id: string;
  title: string;
  type: ReportType;
  date: string; // ISO string
  labName?: string;
  values: LabValue[];
}

interface ReportDetailsProps {
  report: ReportDetailsData | null;
  loading?: boolean;
}

// ---------- Component ----------

export default function ReportDetails({ report, loading = false }: ReportDetailsProps) {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();
  const reportId: string | undefined = route.params?.reportId;

  if (loading || !report) {
    return (
      <View style={styles.centerWrap}>
        <Text style={styles.emptyText}>{loading ? "Loading report…" : "Report not found"}</Text>
      </View>
    );
  }

  const abnormalCount = report.values.filter((v) => v.flag === "Abnormal").length;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <TouchableOpacity style={styles.backRow} onPress={() => navigation.goBack()} activeOpacity={0.7}>
        <ChevronLeft size={20} color={Colors.textSecondary} />
        <Text style={styles.backText}>Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>{report.title}</Text>
      <Text style={styles.subtitle}>
        {report.type} · {dayjs(report.date).format("DD MMM YYYY")}
        {report.labName ? ` · ${report.labName}` : ""}
      </Text>

      {abnormalCount > 0 && (
        <View style={styles.warningBanner}>
          <AlertTriangle size={16} color={Colors.warning} />
          <Text style={styles.warningBannerText}>
            {abnormalCount} value{abnormalCount > 1 ? "s" : ""} outside the reference range
          </Text>
        </View>
      )}

      {/* Lab values */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Lab Values</Text>
        {report.values.map((v, index) => (
          <View key={v.id} style={[styles.valueRow, index < report.values.length - 1 && styles.valueRowBorder]}>
            <View style={styles.valueLeft}>
              <Text style={styles.valueName}>{v.testName}</Text>
              <Text style={styles.valueRange}>
                Reference: {v.referenceLow}–{v.referenceHigh} {v.unit}
              </Text>
            </View>
            <View style={styles.valueRight}>
              <Text
                style={[styles.valueNumber, { color: v.flag === "Abnormal" ? Colors.danger : Colors.text }]}
              >
                {v.value} {v.unit}
              </Text>
              <View
                style={[
                  styles.flagPill,
                  { backgroundColor: (v.flag === "Abnormal" ? Colors.danger : Colors.success) + "20" },
                ]}
              >
                <Text
                  style={[
                    styles.flagPillText,
                    { color: v.flag === "Abnormal" ? Colors.danger : Colors.success },
                  ]}
                >
                  {v.flag}
                </Text>
              </View>
            </View>
          </View>
        ))}
      </View>

      {/* Actions */}
      <View style={styles.actionsRow}>
        <TouchableOpacity
          style={[styles.actionButton, styles.actionButtonPrimary]}
          onPress={() => navigation.navigate("TrendDashboard", { reportId })}
          activeOpacity={0.85}
        >
          <TrendingUp size={18} color={Colors.white} />
          <Text style={styles.actionButtonPrimaryText}>View Trend</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionButton, styles.actionButtonSecondary]}
          onPress={() => navigation.navigate("ChatHome", { reportId })}
          activeOpacity={0.85}
        >
          <Sparkles size={18} color={Colors.primary} />
          <Text style={styles.actionButtonSecondaryText}>Ask AI</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

// ---------- Styles ----------

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: Spacing.md, paddingBottom: Spacing.xxxl },
  centerWrap: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: Colors.background },
  emptyText: { ...Typography.body, color: Colors.textSecondary },
  backRow: { flexDirection: "row", alignItems: "center", marginBottom: Spacing.md },
  backText: { ...Typography.small, color: Colors.textSecondary, marginLeft: 4 },
  title: { ...Typography.pageTitle, fontSize: 22, color: Colors.text },
  subtitle: { ...Typography.small, color: Colors.textSecondary, marginTop: 4, marginBottom: Spacing.md },
  warningBanner: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: Colors.warning + "15",
    borderRadius: 12,
    padding: Spacing.sm,
    marginBottom: Spacing.md,
    gap: Spacing.xs,
  },
  warningBannerText: { ...Typography.small, color: Colors.warning, fontWeight: "600" as const },
  card: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    marginBottom: Spacing.lg,
    shadowColor: Colors.shadow,
    shadowOpacity: 0.04,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 2 },
    elevation: 1,
  },
  cardTitle: { ...Typography.cardTitle, color: Colors.text, marginBottom: Spacing.sm },
  valueRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: Spacing.sm,
  },
  valueRowBorder: { borderBottomWidth: 1, borderBottomColor: Colors.border },
  valueLeft: { flex: 1, paddingRight: Spacing.sm },
  valueName: { ...Typography.body, color: Colors.text, fontWeight: "600" as const },
  valueRange: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  valueRight: { alignItems: "flex-end" },
  valueNumber: { ...Typography.body, fontWeight: "700" as const },
  flagPill: { paddingHorizontal: Spacing.sm, paddingVertical: 2, borderRadius: 20, marginTop: 4 },
  flagPillText: { fontSize: 11, fontWeight: "600" as const },
  actionsRow: { flexDirection: "row", gap: Spacing.sm },
  actionButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    height: 52,
    borderRadius: 12,
    gap: Spacing.xs,
  },
  actionButtonPrimary: { backgroundColor: Colors.primary },
  actionButtonPrimaryText: { ...Typography.body, color: Colors.white, fontWeight: "600" as const },
  actionButtonSecondary: { backgroundColor: Colors.white, borderWidth: 1, borderColor: Colors.primary },
  actionButtonSecondaryText: { ...Typography.body, color: Colors.primary, fontWeight: "600" as const },
});
