/**
 * OCRPreviewScreen.tsx
 * Shown right after a report is uploaded and OCR-processed. Lets the
 * user review/edit extracted values before they're saved as a report.
 *
 * Expected route params: { extractedValues: ExtractedValue[], reportTitle?: string }
 * passed from the upload flow once OCR completes.
 *
 * Uses the real theme exports from src/theme/index.ts:
 *   import { Colors, Spacing, Typography } from '../../theme';
 */

import React, { useState } from "react";
import { View, ScrollView, StyleSheet, TouchableOpacity, TextInput as RNTextInput } from "react-native";
import { Text } from "react-native-paper";
import { useNavigation, useRoute } from "@react-navigation/native";
import { Pencil, Check, X, AlertCircle } from "lucide-react-native";
import { Colors, Spacing, Typography } from "../../theme";
import { Alert } from "react-native";
import { confirmReport } from "../../services/reportService";

// ---------- Types ----------

export interface ExtractedValue {
  id: string;
  testName: string;
  value: string; // kept as string while editable; parse/validate on confirm
  unit: string;
  referenceLow?: number;
  referenceHigh?: number;
  lowConfidence?: boolean; // flag values OCR wasn't sure about
}

interface OCRPreviewScreenProps {
  onConfirm?: (values: ExtractedValue[]) => void;
  onCancel?: () => void;
}

// ---------- Component ----------

export default function OCRPreviewScreen({ onConfirm, onCancel }: OCRPreviewScreenProps) {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();

  const initialValues: ExtractedValue[] = route.params?.extractedValues ?? [];
  console.log("OCR PARAMS:", route.params);
  console.log("INITIAL VALUES:", initialValues);
  const reportTitle: string = route.params?.reportTitle ?? "New Report";

  const [values, setValues] = useState<ExtractedValue[]>(initialValues);
  const [editingId, setEditingId] = useState<string | null>(null);

  const lowConfidenceCount = values.filter((v) => v.lowConfidence).length;

  const updateValue = (id: string, field: "testName" | "value" | "unit", text: string) => {
    setValues((prev) => prev.map((v) => (v.id === id ? { ...v, [field]: text } : v)));
  };

  const handleConfirm = async () => {
  try {
   navigation.navigate("UploadProgress", {
      mode: "confirm",
      tempFileId: route.params.tempFileId,
      labValues: values.map(v => ({
        test_name: v.testName,
        value: Number(v.value),
        unit: v.unit,
        reference_range: [
          v.referenceLow,
          v.referenceHigh,
        ],
      })),
    });

    return;

  } catch (err) {
    console.error(err);
    Alert.alert("Failed to save report");
  }
};

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    } else {
      navigation.goBack();
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Review Extracted Values</Text>
        <Text style={styles.subtitle}>{reportTitle}</Text>

        {lowConfidenceCount > 0 && (
          <View style={styles.warningBanner}>
            <AlertCircle size={16} color={Colors.warning} />
            <Text style={styles.warningBannerText}>
              {lowConfidenceCount} value{lowConfidenceCount > 1 ? "s" : ""} may need a closer look — double
              check before confirming
            </Text>
          </View>
        )}

        {values.length === 0 ? (
          <View style={styles.card}>
            <Text style={styles.emptyText}>No values were extracted. You can go back and retake the photo.</Text>
          </View>
        ) : (
          <View style={styles.card}>
            {values.map((item, index) => {
              const isEditing = editingId === item.id;
              return (
                <View
                  key={item.id}
                  style={[styles.valueRow, index < values.length - 1 && styles.valueRowBorder]}
                >
                  <View style={styles.valueLeft}>
                    {isEditing ? (
                      <RNTextInput
                        style={styles.editInput}
                        value={item.testName}
                        onChangeText={(t) => updateValue(item.id, "testName", t)}
                        placeholder="Test name"
                        placeholderTextColor={Colors.disabled}
                      />
                    ) : (
                      <View style={styles.testNameRow}>
                        <Text style={styles.valueName}>{item.testName}</Text>
                        {item.lowConfidence && <AlertCircle size={14} color={Colors.warning} />}
                      </View>
                    )}
                    {(item.referenceLow !== undefined || item.referenceHigh !== undefined) && (
                      <Text style={styles.valueRange}>
                        Reference: {item.referenceLow ?? "—"}–{item.referenceHigh ?? "—"} {item.unit}
                      </Text>
                    )}
                  </View>

                  <View style={styles.valueRight}>
                    {isEditing ? (
                      <View style={styles.editValueRow}>
                        <RNTextInput
                          style={[styles.editInput, styles.editInputValue]}
                          value={item.value}
                          onChangeText={(t) => updateValue(item.id, "value", t)}
                          keyboardType="numeric"
                          placeholder="0"
                          placeholderTextColor={Colors.disabled}
                        />
                        <RNTextInput
                          style={[styles.editInput, styles.editInputUnit]}
                          value={item.unit}
                          onChangeText={(t) => updateValue(item.id, "unit", t)}
                          placeholder="unit"
                          placeholderTextColor={Colors.disabled}
                        />
                      </View>
                    ) : (
                      <Text style={styles.valueNumber}>
                        {item.value} {item.unit}
                      </Text>
                    )}
                  </View>

                  <TouchableOpacity
                    style={styles.editIconButton}
                    onPress={() => setEditingId(isEditing ? null : item.id)}
                    hitSlop={8}
                  >
                    {isEditing ? (
                      <Check size={18} color={Colors.success} />
                    ) : (
                      <Pencil size={16} color={Colors.textSecondary} />
                    )}
                  </TouchableOpacity>
                </View>
              );
            })}
          </View>
        )}
      </ScrollView>

      {/* Actions */}
      <View style={styles.actionsBar}>
        <TouchableOpacity style={[styles.actionButton, styles.cancelButton]} onPress={handleCancel} activeOpacity={0.85}>
          <X size={18} color={Colors.danger} />
          <Text style={styles.cancelButtonText}>Cancel</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionButton, styles.confirmButton]}
          onPress={handleConfirm}
          activeOpacity={0.85}
          disabled={values.length === 0}
        >
          <Check size={18} color={Colors.white} />
          <Text style={styles.confirmButtonText}>Confirm</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// ---------- Styles ----------

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: Spacing.md, paddingBottom: Spacing.xxl },
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
  warningBannerText: { ...Typography.small, color: Colors.warning, flex: 1 },
  card: {
    backgroundColor: Colors.card,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
  },
  emptyText: { ...Typography.small, color: Colors.textSecondary, textAlign: "center" },
  valueRow: { flexDirection: "row", alignItems: "center", paddingVertical: Spacing.sm },
  valueRowBorder: { borderBottomWidth: 1, borderBottomColor: Colors.border },
  valueLeft: { flex: 1, paddingRight: Spacing.sm },
  testNameRow: { flexDirection: "row", alignItems: "center", gap: 6 },
  valueName: { ...Typography.body, color: Colors.text, fontWeight: "600" as const },
  valueRange: { ...Typography.caption, color: Colors.textSecondary, marginTop: 2 },
  valueRight: { alignItems: "flex-end", marginRight: Spacing.sm },
  valueNumber: { ...Typography.body, color: Colors.text, fontWeight: "700" as const },
  editInput: {
    ...Typography.body,
    color: Colors.text,
    borderWidth: 1,
    borderColor: Colors.primary,
    borderRadius: 12,
    paddingHorizontal: Spacing.sm,
    paddingVertical: 6,
    minWidth: 100,
  },
  editValueRow: { flexDirection: "row", gap: Spacing.xs },
  editInputValue: { minWidth: 64 },
  editInputUnit: { minWidth: 60 },
  editIconButton: { padding: Spacing.xs },
  actionsBar: {
    flexDirection: "row",
    gap: Spacing.sm,
    padding: Spacing.md,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
    backgroundColor: Colors.card,
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
  cancelButton: { backgroundColor: Colors.white, borderWidth: 1, borderColor: Colors.danger },
  cancelButtonText: { ...Typography.body, color: Colors.danger, fontWeight: "600" as const },
  confirmButton: { backgroundColor: Colors.primary },
  confirmButtonText: { ...Typography.body, color: Colors.white, fontWeight: "600" as const },
});
