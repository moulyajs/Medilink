import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useRoute, useNavigation } from "@react-navigation/native";
import {
  uploadReport,
  confirmReport,
} from "../../services/reportService";

export default function UploadProgressScreen() {
  const route = useRoute<any>();
  const navigation = useNavigation<any>();

  const {
    file,
    mode,
    tempFileId,
    labValues,
  } = route.params || {};

  console.log("MODE =", mode);
  console.log("FILE =", file);
  console.log("TEMP FILE ID =", tempFileId);
  console.log("LAB VALUES =", labValues);

  const [status, setStatus] = useState("Uploading...");
  const [duplicate, setDuplicate] = useState(false);

  useEffect(() => {
    startUpload();
  }, []);

  const startUpload = async () => {
    try {
      let response: any;

      // =====================================================
      // CONFIRM MODE
      // =====================================================

      if (mode === "confirm") {
        setStatus("Saving report...");

        console.log(
          "========== CONFIRMING REPORT =========="
        );

        console.log(
          "TEMP FILE ID:",
          tempFileId
        );

        console.log(
          "LAB VALUES:",
          JSON.stringify(
            labValues,
            null,
            2
          )
        );

        console.log(
          "======================================="
        );

        if (!tempFileId) {
          Alert.alert(
            "Error",
            "Temporary file ID is missing. Please upload the report again."
          );

          navigation.goBack();
          return;
        }

        if (
          !labValues ||
          !Array.isArray(labValues) ||
          labValues.length === 0
        ) {
          Alert.alert(
            "Error",
            "No lab values were found. Please upload the report again."
          );

          navigation.goBack();
          return;
        }

        response = await confirmReport(
          tempFileId,
          labValues
        );

        console.log(
          "========== CONFIRM RESPONSE =========="
        );

        console.log(
          JSON.stringify(
            response,
            null,
            2
          )
        );

        console.log(
          "======================================"
        );

        // Duplicate report
        if (response?.is_duplicate) {
          Alert.alert(
            "Duplicate Report",
            "This report has already been saved."
          );

          navigation.goBack();
          return;
        }

        // Successfully saved
        navigation.replace(
          "UploadCompleted"
        );

        return;
      }

      // =====================================================
      // NORMAL UPLOAD MODE
      // =====================================================

      setStatus("Uploading...");

      const timer = setTimeout(() => {
        setStatus("Extracting...");
      }, 1000);

      try {
        response = await uploadReport(file);

        // ===================================================
        // DEBUG UPLOAD RESPONSE
        // ===================================================

        console.log(
          "========== UPLOAD RESPONSE =========="
        );

        console.log(
          "FULL RESPONSE:",
          JSON.stringify(
            response,
            null,
            2
          )
        );

        console.log(
          "TEMP FILE ID:",
          response?.temp_file_id
        );

        console.log(
          "LAB VALUES:",
          response?.lab_values
        );

        console.log(
          "LAB VALUES COUNT:",
          response?.lab_values?.length
        );

        console.log(
          "IS DUPLICATE:",
          response?.is_duplicate
        );

        console.log(
          "===================================="
        );

      } finally {
        clearTimeout(timer);
      }

      // =====================================================
      // DUPLICATE DETECTED
      // =====================================================

      if (response?.is_duplicate) {
        console.log(
          "DUPLICATE REPORT DETECTED"
        );

        setDuplicate(true);
        return;
      }

      // =====================================================
      // PREPARE OCR VALUES
      // =====================================================

      const extractedValues =
        (response?.lab_values || []).map(
          (lab: any, index: number) => ({
            ...lab,

            // UI ID
            id: String(index + 1),

            // Test name
            testName:
              lab.test_name ||
              lab.test ||
              "Unknown Test",

            // Value
            value:
              lab.value !== undefined &&
              lab.value !== null
                ? String(lab.value)
                : "",

            // Unit
            unit:
              lab.unit || "",

            // Reference range
            referenceLow:
              lab.reference_range?.[0] ??
              undefined,

            referenceHigh:
              lab.reference_range?.[1] ??
              undefined,

            // Confidence
            lowConfidence: false,
          })
        );

      // =====================================================
      // DEBUG OCR NAVIGATION
      // =====================================================

      console.log(
        "========== OCR NAVIGATION =========="
      );

      console.log(
        "TEMP FILE ID:",
        response?.temp_file_id
      );

      console.log(
        "EXTRACTED VALUES:",
        JSON.stringify(
          extractedValues,
          null,
          2
        )
      );

      console.log(
        "EXTRACTED VALUES COUNT:",
        extractedValues.length
      );

      console.log(
        "===================================="
      );

      // =====================================================
      // CHECK TEMP FILE ID
      // =====================================================

      if (!response?.temp_file_id) {
        console.error(
          "TEMP FILE ID IS MISSING"
        );

        Alert.alert(
          "Upload Error",
          "The server did not return a temporary file ID."
        );

        navigation.goBack();
        return;
      }

      // =====================================================
      // OPEN OCR PREVIEW
      // =====================================================

      navigation.replace(
        "OCRPreview",
        {
          tempFileId:
            response.temp_file_id,

          extractedValues:
            extractedValues,

          reportTitle:
            "Lab Report",
        }
      );

      console.log(
        "OCRPreview navigation called successfully"
      );

      return;

    } catch (error: any) {

      console.error(
        "========== UPLOAD/CONFIRM ERROR =========="
      );

      console.error(
        "ERROR:",
        error
      );

      console.error(
        "ERROR MESSAGE:",
        error?.message
      );

      console.error(
        "ERROR RESPONSE:",
        error?.response
      );

      console.error(
        "ERROR STATUS:",
        error?.response?.status
      );

      console.error(
        "ERROR DATA:",
        error?.response?.data
      );

      console.error(
        "=========================================="
      );

      Alert.alert(
        "Upload Failed",
        error?.response?.data?.detail ||
          error?.message ||
          "Upload failed."
      );

      navigation.goBack();
    }
  };

  // =======================================================
  // DUPLICATE SCREEN
  // =======================================================

  if (duplicate) {
    return (
      <SafeAreaView
        style={styles.container}
      >
        <Text style={styles.title}>
          Duplicate Report
        </Text>

        <Text style={styles.subtitle}>
          This report has already been
          uploaded.
        </Text>

        <Text
          style={styles.goBack}
          onPress={() =>
            navigation.goBack()
          }
        >
          ← Go Back
        </Text>
      </SafeAreaView>
    );
  }

  // =======================================================
  // LOADING SCREEN
  // =======================================================

  return (
    <SafeAreaView
      style={styles.container}
    >
      <ActivityIndicator
        size="large"
        color="#2563EB"
      />

      <Text style={styles.title}>
        {status}
      </Text>

      <Text style={styles.subtitle}>
        Please don't close the app.
      </Text>
    </SafeAreaView>
  );
}

// =========================================================
// STYLES
// =========================================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    padding: 24,
  },

  title: {
    marginTop: 30,
    fontSize: 24,
    fontWeight: "700",
    color: "#2563EB",
    textAlign: "center",
  },

  subtitle: {
    marginTop: 12,
    color: "#64748B",
    fontSize: 16,
    textAlign: "center",
  },

  goBack: {
    marginTop: 30,
    fontSize: 18,
    fontWeight: "700",
    color: "#2563EB",
  },
});