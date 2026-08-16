import React, { useState } from "react";
import {
  View,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  TextInput as RNTextInput,
  Alert,
} from "react-native";
import { Text } from "react-native-paper";
import { useNavigation, useRoute } from "@react-navigation/native";
import {
  Pencil,
  Check,
  X,
  AlertCircle,
} from "lucide-react-native";
import { Colors, Spacing, Typography } from "../../theme";

// ---------- Types ----------

export interface ExtractedValue {
  id: string;

  testName: string;
  value: string;
  unit: string;

  referenceLow?: number;
  referenceHigh?: number;

  lowConfidence?: boolean;

  test?: string;
  date?: string;
  abnormal?: boolean;
  status?: string;
}

interface OCRPreviewScreenProps {
  onConfirm?: (values: ExtractedValue[]) => void;
  onCancel?: () => void;
}

// ---------- Component ----------

export default function OCRPreviewScreen({
  onConfirm,
  onCancel,
}: OCRPreviewScreenProps) {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();

  // -----------------------------------------
  // GET ROUTE PARAMETERS SAFELY
  // -----------------------------------------

  const params = route.params ?? {};

  const initialValues: ExtractedValue[] =
    params.extractedValues ?? [];

  const reportTitle: string =
    params.reportTitle ?? "New Report";

  const tempFileId: string | undefined =
    params.tempFileId;

  // -----------------------------------------
  // DEBUG
  // -----------------------------------------

  console.log("========== OCR PREVIEW ==========");
  console.log("TEMP FILE ID:", tempFileId);
  console.log("TEMP FILE ID TYPE:", typeof tempFileId);
  console.log("VALUES COUNT:", initialValues.length);
  console.log(
    "ROUTE PARAMS:",
    JSON.stringify(params, null, 2)
  );
  console.log("=================================");

  const [values, setValues] =
    useState<ExtractedValue[]>(initialValues);

  const [editingId, setEditingId] =
    useState<string | null>(null);

  const [saving, setSaving] =
    useState(false);

  const lowConfidenceCount =
    values.filter((v) => v.lowConfidence).length;

  // -----------------------------------------
  // UPDATE VALUE
  // -----------------------------------------

  const updateValue = (
    id: string,
    field: "testName" | "value" | "unit",
    text: string
  ) => {
    setValues((prev) =>
      prev.map((v) =>
        v.id === id
          ? {
              ...v,
              [field]: text,
            }
          : v
      )
    );
  };

  // -----------------------------------------
  // CONFIRM REPORT
  // -----------------------------------------

  const handleConfirm = async () => {
    if (saving) {
      return;
    }

    console.log(
      "========== CONFIRM REPORT =========="
    );

    console.log(
      "TEMP FILE ID:",
      tempFileId
    );

    console.log(
      "VALUES COUNT:",
      values.length
    );

    console.log(
      "VALUES:",
      JSON.stringify(values, null, 2)
    );

    console.log(
      "===================================="
    );

    // -----------------------------------------
    // CHECK TEMP FILE ID
    // -----------------------------------------

    if (!tempFileId) {
      Alert.alert(
        "Upload Error",
        "Temporary file ID is missing. Please upload the report again."
      );

      console.error(
        "TEMP FILE ID IS MISSING"
      );

      return;
    }

    // -----------------------------------------
    // CHECK LAB VALUES
    // -----------------------------------------

    if (values.length === 0) {
      Alert.alert(
        "No Values",
        "No lab values were extracted from this report."
      );

      return;
    }

    // -----------------------------------------
    // VALIDATE VALUES
    // -----------------------------------------

    for (const v of values) {
      if (
        !v.value ||
        v.value.trim() === ""
      ) {
        Alert.alert(
          "Missing Value",
          `${v.testName} has no value.`
        );

        return;
      }

      if (isNaN(Number(v.value))) {
        Alert.alert(
          "Invalid Value",
          `${v.testName} must be a number.`
        );

        return;
      }
    }

    setSaving(true);

    try {
      // -----------------------------------------
      // BUILD BACKEND PAYLOAD
      // -----------------------------------------

      const payload = values.map((v) => ({
        test_name:
          v.test ||
          v.testName,

        value:
          Number(v.value),

        unit:
          v.unit ||
          null,

        reference_range:
          v.referenceLow != null &&
          v.referenceHigh != null
            ? [
                Number(v.referenceLow),
                Number(v.referenceHigh),
              ]
            : null,

        abnormal:
          v.abnormal ??
          false,

        status:
          v.status ??
          null,

        date:
          v.date ??
          null,
      }));

      console.log(
        "========== SENDING CONFIRM =========="
      );

      console.log(
        "TEMP FILE ID:",
        tempFileId
      );

      console.log(
        "PAYLOAD:",
        JSON.stringify(
          payload,
          null,
          2
        )
      );

      console.log(
        "====================================="
      );

      // Optional parent callback
      if (onConfirm) {
        onConfirm(values);
      }

      // -----------------------------------------
      // GO TO UPLOAD PROGRESS
      // -----------------------------------------

      navigation.navigate(
        "UploadProgress",
        {
          mode: "confirm",

          tempFileId:
            tempFileId,

          labValues:
            payload,
        }
      );

    } catch (error: any) {
      console.error(
        "CONFIRM ERROR:",
        error
      );

      setSaving(false);

      Alert.alert(
        "Failed to save report",
        error?.message ||
          "Something went wrong."
      );
    }
  };

  // -----------------------------------------
  // CANCEL
  // -----------------------------------------

  const handleCancel = () => {
    if (saving) {
      return;
    }

    if (onCancel) {
      onCancel();
    } else {
      navigation.goBack();
    }
  };

  // -----------------------------------------
  // UI
  // -----------------------------------------

  return (
    <View style={styles.container}>

      {/* ==============================
          CONTENT
      ============================== */}

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={
          styles.content
        }
        showsVerticalScrollIndicator={true}
      >

        <Text style={styles.title}>
          Review Extracted Values
        </Text>

        <Text style={styles.subtitle}>
          {reportTitle}
        </Text>

        {/* DEBUG INFO */}

        {!tempFileId && (
          <View
            style={styles.errorBanner}
          >
            <AlertCircle
              size={18}
              color={Colors.danger}
            />

            <Text
              style={
                styles.errorBannerText
              }
            >
              Temporary file ID is missing.
              Please upload this report again.
            </Text>
          </View>
        )}

        {/* LOW CONFIDENCE */}

        {lowConfidenceCount > 0 && (
          <View
            style={
              styles.warningBanner
            }
          >
            <AlertCircle
              size={16}
              color={Colors.warning}
            />

            <Text
              style={
                styles.warningBannerText
              }
            >
              {lowConfidenceCount} value
              {lowConfidenceCount > 1
                ? "s"
                : ""} may need a closer look.
              Double-check before confirming.
            </Text>
          </View>
        )}

        {/* VALUES */}

        {values.length === 0 ? (
          <View style={styles.card}>
            <Text
              style={styles.emptyText}
            >
              No values were extracted.
              You can go back and upload
              the report again.
            </Text>
          </View>
        ) : (
          <View style={styles.card}>

            {values.map(
              (item, index) => {

                const isEditing =
                  editingId === item.id;

                return (
                  <View
                    key={item.id}
                    style={[
                      styles.valueRow,
                      index <
                        values.length - 1 &&
                        styles.valueRowBorder,
                    ]}
                  >

                    {/* LEFT */}

                    <View
                      style={
                        styles.valueLeft
                      }
                    >

                      {isEditing ? (
                        <RNTextInput
                          style={
                            styles.editInput
                          }
                          value={
                            item.testName
                          }
                          onChangeText={(
                            text
                          ) =>
                            updateValue(
                              item.id,
                              "testName",
                              text
                            )
                          }
                          placeholder="Test name"
                          placeholderTextColor={
                            Colors.disabled
                          }
                        />
                      ) : (
                        <View
                          style={
                            styles.testNameRow
                          }
                        >
                          <Text
                            style={
                              styles.valueName
                            }
                          >
                            {
                              item.testName
                            }
                          </Text>

                          {item.lowConfidence && (
                            <AlertCircle
                              size={14}
                              color={
                                Colors.warning
                              }
                            />
                          )}
                        </View>
                      )}

                      {(item.referenceLow !==
                        undefined ||
                        item.referenceHigh !==
                          undefined) && (
                        <Text
                          style={
                            styles.valueRange
                          }
                        >
                          Reference:{" "}
                          {item.referenceLow ??
                            "—"}
                          {" – "}
                          {item.referenceHigh ??
                            "—"}{" "}
                          {item.unit}
                        </Text>
                      )}

                    </View>

                    {/* RIGHT */}

                    <View
                      style={
                        styles.valueRight
                      }
                    >

                      {isEditing ? (
                        <View
                          style={
                            styles.editValueRow
                          }
                        >

                          <RNTextInput
                            style={[
                              styles.editInput,
                              styles.editInputValue,
                            ]}
                            value={
                              item.value
                            }
                            onChangeText={(
                              text
                            ) =>
                              updateValue(
                                item.id,
                                "value",
                                text
                              )
                            }
                            keyboardType="numeric"
                            placeholder="0"
                          />

                          <RNTextInput
                            style={[
                              styles.editInput,
                              styles.editInputUnit,
                            ]}
                            value={
                              item.unit
                            }
                            onChangeText={(
                              text
                            ) =>
                              updateValue(
                                item.id,
                                "unit",
                                text
                              )
                            }
                            placeholder="unit"
                          />

                        </View>
                      ) : (
                        <Text
                          style={
                            styles.valueNumber
                          }
                        >
                          {item.value}{" "}
                          {item.unit}
                        </Text>
                      )}

                    </View>

                    {/* EDIT */}

                    <TouchableOpacity
                      style={
                        styles.editIconButton
                      }
                      onPress={() =>
                        setEditingId(
                          isEditing
                            ? null
                            : item.id
                        )
                      }
                    >
                      {isEditing ? (
                        <Check
                          size={18}
                          color={
                            Colors.success
                          }
                        />
                      ) : (
                        <Pencil
                          size={16}
                          color={
                            Colors.textSecondary
                          }
                        />
                      )}
                    </TouchableOpacity>

                  </View>
                );
              }
            )}

          </View>
        )}

      </ScrollView>

      {/* =====================================
          FIXED BOTTOM ACTION BAR
      ===================================== */}

      <View
        style={styles.actionsBar}
      >

        {/* CANCEL */}

        <TouchableOpacity
          style={[
            styles.actionButton,
            styles.cancelButton,
          ]}
          onPress={
            handleCancel
          }
          disabled={saving}
          activeOpacity={0.8}
        >

          <X
            size={20}
            color={
              Colors.danger
            }
          />

          <Text
            style={
              styles.cancelButtonText
            }
          >
            Cancel
          </Text>

        </TouchableOpacity>

        {/* CONFIRM */}

        <TouchableOpacity
          style={[
            styles.actionButton,
            styles.confirmButton,

            saving &&
              styles.disabledButton,
          ]}
          onPress={
            handleConfirm
          }
          disabled={saving}
          activeOpacity={0.8}
        >

          <Check
            size={20}
            color={
              Colors.white
            }
          />

          <Text
            style={
              styles.confirmButtonText
            }
          >
            {saving
              ? "Saving..."
              : "Confirm & Save"}
          </Text>

        </TouchableOpacity>

      </View>

    </View>
  );
}

// ==========================================
// STYLES
// ==========================================

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor:
      Colors.background,
  },

  scroll: {
    flex: 1,
  },

  content: {
    padding: Spacing.md,
    paddingBottom: 140,
  },

  title: {
    ...Typography.pageTitle,
    fontSize: 22,
    color: Colors.text,
  },

  subtitle: {
    ...Typography.small,
    color:
      Colors.textSecondary,
    marginTop: 4,
    marginBottom:
      Spacing.md,
  },

  // -------------------------
  // ERROR BANNER
  // -------------------------

  errorBanner: {
    flexDirection:
      "row",
    alignItems:
      "center",
    backgroundColor:
      "#FEE2E2",
    borderWidth: 1,
    borderColor:
      "#FCA5A5",
    borderRadius: 12,
    padding: Spacing.sm,
    marginBottom:
      Spacing.md,
    gap: 8,
  },

  errorBannerText: {
    flex: 1,
    color: "#B91C1C",
    fontSize: 13,
    fontWeight: "600",
  },

  // -------------------------
  // WARNING
  // -------------------------

  warningBanner: {
    flexDirection:
      "row",
    alignItems:
      "center",
    backgroundColor:
      Colors.warning + "15",
    borderRadius: 12,
    padding:
      Spacing.sm,
    marginBottom:
      Spacing.md,
    gap:
      Spacing.xs,
  },

  warningBannerText: {
    ...Typography.small,
    color:
      Colors.warning,
    flex: 1,
  },

  // -------------------------
  // CARD
  // -------------------------

  card: {
    backgroundColor:
      Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor:
      Colors.border,
    padding:
      Spacing.md,
  },

  emptyText: {
    ...Typography.small,
    color:
      Colors.textSecondary,
    textAlign:
      "center",
  },

  // -------------------------
  // ROW
  // -------------------------

  valueRow: {
    flexDirection:
      "row",
    alignItems:
      "center",
    paddingVertical:
      Spacing.sm,
  },

  valueRowBorder: {
    borderBottomWidth: 1,
    borderBottomColor:
      Colors.border,
  },

  valueLeft: {
    flex: 1,
    paddingRight:
      Spacing.sm,
  },

  testNameRow: {
    flexDirection:
      "row",
    alignItems:
      "center",
    gap: 6,
  },

  valueName: {
    ...Typography.body,
    color:
      Colors.text,
    fontWeight:
      "600" as const,
  },

  valueRange: {
    ...Typography.caption,
    color:
      Colors.textSecondary,
    marginTop: 2,
  },

  valueRight: {
    alignItems:
      "flex-end",
    marginRight:
      Spacing.sm,
  },

  valueNumber: {
    ...Typography.body,
    color:
      Colors.text,
    fontWeight:
      "700" as const,
  },

  // -------------------------
  // EDIT
  // -------------------------

  editInput: {
    ...Typography.body,
    color:
      Colors.text,
    borderWidth: 1,
    borderColor:
      Colors.primary,
    borderRadius: 12,
    paddingHorizontal:
      Spacing.sm,
    paddingVertical: 6,
    minWidth: 100,
    backgroundColor:
      Colors.white,
  },

  editValueRow: {
    flexDirection:
      "row",
    gap:
      Spacing.xs,
  },

  editInputValue: {
    minWidth: 64,
  },

  editInputUnit: {
    minWidth: 60,
  },

  editIconButton: {
    padding:
      Spacing.xs,
  },

  // -------------------------
  // BOTTOM BAR
  // -------------------------

  actionsBar: {
    flexDirection:
      "row",
    gap:
      Spacing.sm,

    paddingHorizontal:
      Spacing.md,

    paddingTop:
      Spacing.md,

    paddingBottom:
      Spacing.lg,

    borderTopWidth: 1,
    borderTopColor:
      Colors.border,

    backgroundColor:
      Colors.card,

    minHeight: 90,

    elevation: 20,

    zIndex: 100,

    position: "relative",
  },

  actionButton: {
    flex: 1,

    flexDirection:
      "row",

    alignItems:
      "center",

    justifyContent:
      "center",

    height: 56,

    borderRadius: 12,

    gap:
      Spacing.xs,
  },

  cancelButton: {
    backgroundColor:
      Colors.white,

    borderWidth: 1,

    borderColor:
      Colors.danger,
  },

  cancelButtonText: {
    ...Typography.body,
    color:
      Colors.danger,
    fontWeight:
      "600" as const,
  },

  confirmButton: {
    backgroundColor:
      Colors.primary,

    opacity: 1,
  },

  confirmButtonText: {
    ...Typography.body,
    color:
      Colors.white,
    fontWeight:
      "700" as const,
  },

  disabledButton: {
    opacity: 0.5,
  },
});