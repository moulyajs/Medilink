/**
 * PersonalBaseline.tsx
 * Shows a person's individual statistical baseline for a given health
 * metric: personal average, personal range, personal variability,
 * historical mean, and standard deviation. This is distinct from the
 * clinical reference range — it's "what's normal for this person."
 *
 * Expected route param: { metricName: string } (e.g. "Hemoglobin"),
 * usually reached from a Test Detail screen.
 *
 * Uses the real theme exports from src/theme/index.ts:
 *   import { Colors, Spacing, Typography } from '../../theme';
 */

import React from "react";
import { View, ScrollView, StyleSheet } from "react-native";
import { Text } from "react-native-paper";
import { useRoute } from "@react-navigation/native";
import { LineChart } from "react-native-gifted-charts";
import { Info } from "lucide-react-native";
import { Colors, Spacing, Typography } from "../../theme";

// ---------- Types ----------

export interface BaselineHistoryPoint {
  date: string; // ISO string
  value: number;
}

export interface PersonalBaselineData {
  metricName: string;
  unit: string;
  personalAverage: number;
  personalRangeLow: number;
  personalRangeHigh: number;
  personalVariability: number; // e.g. coefficient of variation, as a %
  historicalMean: number;
  standardDeviation: number;
  history: BaselineHistoryPoint[];
}

interface PersonalBaselineProps {
  data: PersonalBaselineData | null;
  loading?: boolean;
}

// ---------- Small stat card ----------

function StatCard({
  label,
  value,
  unit,
  helper,
}: {
  label: string;
  value: string | number;
  unit?: string;
  helper?: string;
}) {
  return (
    <View style={styles.statCard}>
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={styles.statValue}>
        {value}
        {unit ? <Text style={styles.statUnit}> {unit}</Text> : null}
      </Text>
      {helper && <Text style={styles.statHelper}>{helper}</Text>}
    </View>
  );
}

// ---------- Component ----------

export default function PersonalBaseline({ data, loading = false }: PersonalBaselineProps) {
  const route = useRoute<any>();
  const metricName: string | undefined = route.params?.metricName;

  if (loading || !data) {
    return (
      <View style={styles.centerWrap}>
        <Text style={styles.emptyText}>
          {loading ? "Loading baseline…" : `No baseline data available${metricName ? ` for ${metricName}` : ""}`}
        </Text>
      </View>
    );
  }

  const chartData = data.history.map((point) => ({ value: point.value }));

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{data.metricName}</Text>
      <Text style={styles.subtitle}>Personal baseline</Text>

      {/* Explainer banner */}
      <View style={styles.infoBanner}>
        <Info size={16} color={Colors.primary} />
        <Text style={styles.infoBannerText}>
          This reflects what's typical for you specifically, based on your own history — not the general
          clinical reference range.
        </Text>
      </View>

      {/* Trend chart */}
      {chartData.length > 1 && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>History</Text>
          <LineChart
            data={chartData}
            color={Colors.primary}
            thickness={2}
            hideDataPoints={false}
            dataPointsColor={Colors.primary}
            yAxisTextStyle={{ color: Colors.textSecondary, fontSize: 11 }}
            xAxisLabelTextStyle={{ color: Colors.textSecondary, fontSize: 11 }}
            noOfSections={4}
            areaChart
            startFillColor={Colors.primary}
            startOpacity={0.15}
            endOpacity={0.02}
            initialSpacing={8}
            height={160}
          />
        </View>
      )}

      {/* Stat grid */}
      <View style={styles.statGrid}>
        <StatCard label="Personal Average" value={data.personalAverage} unit={data.unit} />
        <StatCard
          label="Personal Range"
          value={`${data.personalRangeLow}–${data.personalRangeHigh}`}
          unit={data.unit}
        />
        <StatCard label="Personal Variability" value={`${data.personalVariability}%`} helper="Coefficient of variation" />
        <StatCard label="Historical Mean" value={data.historicalMean} unit={data.unit} />
        <StatCard label="Standard Deviation" value={data.standardDeviation} unit={data.unit} />
      </View>
    </ScrollView>
  );
}

// ---------- Styles ----------

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: Spacing.md, paddingBottom: Spacing.xxxl },
  centerWrap: { flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: Colors.background, padding: Spacing.md },
  emptyText: { ...Typography.body, color: Colors.textSecondary, textAlign: "center" },
  title: { ...Typography.pageTitle, fontSize: 22, color: Colors.text },
  subtitle: { ...Typography.small, color: Colors.textSecondary, marginTop: 4, marginBottom: Spacing.md },
  infoBanner: {
    flexDirection: "row",
    alignItems: "flex-start",
    backgroundColor: Colors.primary + "12",
    borderRadius: 12,
    padding: Spacing.sm,
    marginBottom: Spacing.md,
    gap: Spacing.xs,
  },
  infoBannerText: { ...Typography.caption, color: Colors.text, flex: 1, lineHeight: 16 },
  card: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    marginBottom: Spacing.md,
  },
  cardTitle: { ...Typography.cardTitle, color: Colors.text, marginBottom: Spacing.sm },
  statGrid: { flexDirection: "row", flexWrap: "wrap", gap: Spacing.sm },
  statCard: {
    width: "47%",
    backgroundColor: Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.sm,
  },
  statLabel: { ...Typography.caption, color: Colors.textSecondary },
  statValue: { ...Typography.cardTitle, color: Colors.text, marginTop: 4 },
  statUnit: { ...Typography.small, color: Colors.textSecondary, fontWeight: "400" as const },
  statHelper: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
});
