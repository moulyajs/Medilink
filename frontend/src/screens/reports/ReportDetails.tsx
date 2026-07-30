/**
 * ReportDetails.tsx
 * Displays report details fetched from backend.
 */

import React, { useEffect, useState } from "react";
import {
  View,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
} from "react-native";

import { Text, ActivityIndicator } from "react-native-paper";

import {
  useNavigation,
  useRoute,
} from "@react-navigation/native";

import {
  TrendingUp,
  Sparkles,
  ChevronLeft,
  AlertTriangle,
} from "lucide-react-native";

import dayjs from "dayjs";

import {
  Colors,
  Spacing,
  Typography,
} from "../../theme";

import {
  getReportById,
  ReportDetail,
} from "../../services/reportService";

interface RouteParams {
  documentId: string;
}

export default function ReportDetails() {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();

  const { documentId } =
    route.params as RouteParams;

  const [loading, setLoading] =
    useState(true);

  const [report, setReport] =
    useState<ReportDetail | null>(null);

  useEffect(() => {
    loadReport();
  }, []);

  const loadReport = async () => {
    try {
      setLoading(true);

      const data =
        await getReportById(documentId);

      console.log(
        "REPORT DETAILS",
        data
      );

      setReport(data);
    } catch (err) {
      console.error(
        "Failed to load report:",
        err
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.centerWrap}>
        <ActivityIndicator
          size="large"
        />
      </View>
    );
  }

  if (!report) {
    return (
      <View style={styles.centerWrap}>
        <Text style={styles.emptyText}>
          Report not found
        </Text>
      </View>
    );
  }

  const abnormalCount =
    report.lab_values.filter(
      (item: any) =>
        item.abnormal_flag
    ).length;

  return (
        <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
    >
      <TouchableOpacity
        style={styles.backRow}
        activeOpacity={0.7}
        onPress={() => navigation.goBack()}
      >
        <ChevronLeft
          size={20}
          color={Colors.textSecondary}
        />

        <Text style={styles.backText}>
          Back
        </Text>
      </TouchableOpacity>

      <Text style={styles.title}>
        {report.document_type.replace(
          "_",
          " "
        )}
      </Text>

      <Text style={styles.subtitle}>
        {dayjs(report.upload_date).format(
          "DD MMM YYYY"
        )}
      </Text>

      {abnormalCount > 0 && (
        <View style={styles.warningBanner}>
          <AlertTriangle
            size={16}
            color={Colors.warning}
          />

          <Text
            style={
              styles.warningBannerText
            }
          >
            {abnormalCount} abnormal
            {abnormalCount > 1
              ? " values"
              : " value"}
          </Text>
        </View>
      )}

      <View style={styles.card}>
        <Text style={styles.cardTitle}>
          Lab Values
        </Text>

        {report.lab_values.length === 0 ? (
          <Text style={styles.emptyText}>
            No lab values found.
          </Text>
        ) : (
          report.lab_values.map(
            (
              item: any,
              index: number
            ) => (
              <View
                key={item.result_id}
                style={[
                  styles.valueRow,
                  index <
                    report.lab_values
                      .length -
                      1 &&
                    styles.valueRowBorder,
                ]}
              >
                <View
                  style={styles.valueLeft}
                >
                  <Text
                    style={
                      styles.valueName
                    }
                  >
                    {item.test_name}
                  </Text>

                  <Text
                    style={
                      styles.valueRange
                    }
                  >
                    Reference:{" "}
                    {item.reference_low} –
                    {" "}
                    {item.reference_high}
                    {" "}
                    {item.unit}
                  </Text>

                  <Text
                    style={
                      styles.valueRange
                    }
                  >
                    {dayjs(
                      item.result_date
                    ).format(
                      "DD MMM YYYY"
                    )}
                  </Text>
                </View>

                <View
                  style={
                    styles.valueRight
                  }
                >
                  <Text
                    style={[
                      styles.valueNumber,
                      {
                        color:
                          item.abnormal_flag
                            ? Colors.danger
                            : Colors.text,
                      },
                    ]}
                  >
                    {item.value}{" "}
                    {item.unit}
                  </Text>

                  <View
                    style={[
                      styles.flagPill,
                      {
                        backgroundColor:
                          (
                            item.abnormal_flag
                              ? Colors.danger
                              : Colors.success
                          ) + "20",
                      },
                    ]}
                  >
                    <Text
                      style={[
                        styles.flagPillText,
                        {
                          color:
                            item.abnormal_flag
                              ? Colors.danger
                              : Colors.success,
                        },
                      ]}
                    >
                      {item.abnormal_flag
                        ? "Abnormal"
                        : "Normal"}
                    </Text>
                  </View>
                </View>
              </View>
            )
          )
        )}
      </View>
            <View style={styles.actionsRow}>
        <TouchableOpacity
          style={[
            styles.actionButton,
            styles.actionButtonPrimary,
          ]}
          activeOpacity={0.85}
          onPress={() =>
            navigation.navigate(
              "Trend",
              {
                documentId,
              }
            )
          }
        >
          <TrendingUp
            size={18}
            color={Colors.white}
          />

          <Text
            style={
              styles.actionButtonPrimaryText
            }
          >
            View Trend
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.actionButton,
            styles.actionButtonSecondary,
          ]}
          activeOpacity={0.85}
          onPress={() =>
            navigation.navigate(
              "ChatHome",
              {
                documentId,
              }
            )
          }
        >
          <Sparkles
            size={18}
            color={Colors.primary}
          />

          <Text
            style={
              styles.actionButtonSecondaryText
            }
          >
            Ask AI
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },

  content: {
    padding: Spacing.md,
    paddingBottom: Spacing.xxxl,
  },

  centerWrap: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: Colors.background,
  },

  emptyText: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: "center",
  },

  backRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: Spacing.md,
  },

  backText: {
    ...Typography.small,
    color: Colors.textSecondary,
    marginLeft: 4,
  },

  title: {
    ...Typography.pageTitle,
    fontSize: 22,
    color: Colors.text,
  },

  subtitle: {
    ...Typography.small,
    color: Colors.textSecondary,
    marginTop: 4,
    marginBottom: Spacing.md,
  },

  warningBanner: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor:
      Colors.warning + "15",
    borderRadius: 12,
    padding: Spacing.sm,
    marginBottom: Spacing.md,
    gap: Spacing.xs,
  },

  warningBannerText: {
    ...Typography.small,
    color: Colors.warning,
    fontWeight: "600",
  },

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
    shadowOffset: {
      width: 0,
      height: 2,
    },
    elevation: 1,
  },

  cardTitle: {
    ...Typography.cardTitle,
    color: Colors.text,
    marginBottom: Spacing.sm,
  },

  valueRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: Spacing.sm,
  },

  valueRowBorder: {
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },

  valueLeft: {
    flex: 1,
    paddingRight: Spacing.sm,
  },

  valueName: {
    ...Typography.body,
    color: Colors.text,
    fontWeight: "600",
  },

  valueRange: {
    ...Typography.caption,
    color: Colors.textSecondary,
    marginTop: 2,
  },

  valueRight: {
    alignItems: "flex-end",
  },

  valueNumber: {
    ...Typography.body,
    fontWeight: "700",
  },

  flagPill: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: 2,
    borderRadius: 20,
    marginTop: 4,
  },

  flagPillText: {
    fontSize: 11,
    fontWeight: "600",
  },

  actionsRow: {
    flexDirection: "row",
    gap: Spacing.sm,
  },

  actionButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    height: 52,
    borderRadius: 12,
    gap: Spacing.xs,
  },

  actionButtonPrimary: {
    backgroundColor: Colors.primary,
  },

  actionButtonPrimaryText: {
    ...Typography.body,
    color: Colors.white,
    fontWeight: "600",
  },

  actionButtonSecondary: {
    backgroundColor: Colors.white,
    borderWidth: 1,
    borderColor: Colors.primary,
  },

  actionButtonSecondaryText: {
    ...Typography.body,
    color: Colors.primary,
    fontWeight: "600",
  },
});