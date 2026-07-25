/**
 * ReportsList.tsx
 * Fetches reports from backend and displays them with
 * search and filter support.
 */

import React, { useEffect, useMemo, useState } from "react";
import { View, FlatList, StyleSheet, TouchableOpacity } from "react-native";
import { Text, Searchbar, Chip, ActivityIndicator } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import {
  FileText,
  Activity,
  ScanLine,
  Pill,
  FileQuestion,
} from "lucide-react-native";
import dayjs from "dayjs";

import { Colors, Spacing, Typography } from "../../theme";
import {
  getReports,
  ReportListItem,
} from "../../services/reportService";

// -----------------------------
// Types
// -----------------------------

type ReportFilter =
  | "All"
  | "lab_report"
  | "ecg"
  | "xray"
  | "prescription";

// -----------------------------
// Filter Chips
// -----------------------------

const FILTERS: ReportFilter[] = [
  "All",
  "lab_report",
  "ecg",
  "xray",
  "prescription",
];

// -----------------------------
// Icons
// -----------------------------

const TYPE_ICON: Record<
  string,
  React.ComponentType<{ size?: number; color?: string }>
> = {
  lab_report: FileText,
  ecg: Activity,
  xray: ScanLine,
  prescription: Pill,
};

// -----------------------------
// Status Colours
// -----------------------------

const statusColor = (status: string) => {
  switch (status) {
    case "Normal":
      return Colors.success;

    case "Abnormal":
      return Colors.warning;

    case "Pending":
      return Colors.danger;

    default:
      return Colors.textSecondary;
  }
};

// -----------------------------
// Component
// -----------------------------

export default function ReportsList() {
  const navigation = useNavigation<any>();

  const [reports, setReports] = useState<ReportListItem[]>([]);
  const [loading, setLoading] = useState(true);

  const [query, setQuery] = useState("");
  const [activeFilter, setActiveFilter] =
    useState<ReportFilter>("All");

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);

      const data = await getReports();

      setReports(data);
    } catch (err) {
      console.error("Failed to load reports:", err);
    } finally {
      setLoading(false);
    }
  };

  const filteredReports = useMemo(() => {
    return reports.filter((report) => {
      const matchesFilter =
        activeFilter === "All" ||
        report.document_type === activeFilter;

      const matchesQuery =
        report.document_type
          .toLowerCase()
          .includes(query.toLowerCase());

      return matchesFilter && matchesQuery;
    });
  }, [reports, activeFilter, query]);

  return (
    <View style={styles.container}>
      {/* Search */}
      <Searchbar
        placeholder="Search reports"
        value={query}
        onChangeText={setQuery}
        style={styles.searchbar}
        inputStyle={styles.searchbarInput}
        iconColor={Colors.textSecondary}
        placeholderTextColor={Colors.textSecondary}
      />

      {/* Filters */}
      <FlatList
        horizontal
        data={FILTERS}
        keyExtractor={(item) => item}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.filterRow}
        renderItem={({ item }) => {
          const isActive = item === activeFilter;

          return (
            <Chip
              selected={isActive}
              onPress={() => setActiveFilter(item)}
              style={[
                styles.chip,
                isActive && styles.chipActive,
              ]}
              textStyle={[
                styles.chipText,
                isActive && styles.chipTextActive,
              ]}
            >
              {item === "lab_report"
                ? "Lab"
                : item === "ecg"
                ? "ECG"
                : item === "xray"
                ? "X-Ray"
                : item === "prescription"
                ? "Prescription"
                : "All"}
            </Chip>
          );
        }}
      />

      {loading ? (
        <View style={styles.emptyWrap}>
          <ActivityIndicator size="large" />
        </View>
      ) : (
        <FlatList
          data={filteredReports}
          keyExtractor={(item) => item.document_id}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.emptyWrap}>
              <FileQuestion
                size={32}
                color={Colors.disabled}
              />

              <Text style={styles.emptyText}>
                {reports.length === 0
                  ? "No reports uploaded yet"
                  : "No reports match your search"}
              </Text>
            </View>
          }
          renderItem={({ item }) => {
            const Icon =
              TYPE_ICON[item.document_type] || FileText;

            return (
              <TouchableOpacity
                style={styles.card}
                activeOpacity={0.8}
                onPress={() =>
                  navigation.navigate(
                    "ReportDetails",
                    {
                      documentId: item.document_id,
                    }
                  )
                }
              >
                <View style={styles.cardIconWrap}>
                  <Icon
                    size={20}
                    color={Colors.primary}
                  />
                </View>

                <View style={styles.cardBody}>
                  <Text
                    style={styles.cardTitle}
                    numberOfLines={1}
                  >
                    {item.document_type}
                  </Text>

                  <Text style={styles.cardMeta}>
                    {dayjs(item.upload_date).format(
                      "DD MMM YYYY"
                    )}
                  </Text>
                </View>

                <View
                  style={[
                    styles.statusPill,
                    {
                      backgroundColor:
                        statusColor(item.status) + "20",
                    },
                  ]}
                >
                  <Text
                    style={[
                      styles.statusPillText,
                      {
                        color: statusColor(item.status),
                      },
                    ]}
                  >
                    {item.status}
                  </Text>
                </View>
              </TouchableOpacity>
            );
          }}
                  />
      )}
    </View>
  );
}

// ---------- Styles ----------

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    padding: Spacing.md,
  },

  searchbar: {
    backgroundColor: Colors.card,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: Colors.border,
    elevation: 0,
    marginBottom: Spacing.md,
  },

  searchbarInput: {
    ...Typography.body,
    color: Colors.text,
    minHeight: 0,
  },

  filterRow: {
    paddingBottom: Spacing.md,
    gap: Spacing.xs,
  },

  chip: {
    backgroundColor: Colors.card,
    borderWidth: 1,
    borderColor: Colors.border,
    marginRight: Spacing.xs,
  },

  chipActive: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },

  chipText: {
    ...Typography.small,
    color: Colors.text,
  },

  chipTextActive: {
    color: Colors.white,
    fontWeight: "600" as const,
  },

  listContent: {
    paddingBottom: Spacing.xxxl,
  },

  card: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    marginBottom: Spacing.sm,
    shadowColor: Colors.shadow,
    shadowOpacity: 0.04,
    shadowRadius: 6,
    shadowOffset: {
      width: 0,
      height: 2,
    },
    elevation: 1,
  },

  cardIconWrap: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: Colors.background,
    alignItems: "center",
    justifyContent: "center",
    marginRight: Spacing.sm,
  },

  cardBody: {
    flex: 1,
  },

  cardTitle: {
    ...Typography.cardTitle,
    fontSize: 16,
    color: Colors.text,
  },

  cardMeta: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 2,
  },

  statusPill: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 4,
    borderRadius: 20,
    marginLeft: Spacing.sm,
  },

  statusPillText: {
    fontSize: 11,
    fontWeight: "600" as const,
  },

  emptyWrap: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: Spacing.xxl,
    gap: Spacing.sm,
  },

  emptyText: {
    ...Typography.small,
    color: Colors.textSecondary,
    textAlign: "center",
  },
});
