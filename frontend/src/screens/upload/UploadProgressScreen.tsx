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
  } = route.params;

  console.log("MODE =", mode);

  const [status, setStatus] = useState("Uploading...");
  const [duplicate, setDuplicate] = useState(false);

  useEffect(() => {
    startUpload();
  }, []);

  const startUpload = async () => {
  try {
    let response;

    if (mode === "confirm") {
      setStatus("Saving report...");

      response = await confirmReport(
        tempFileId,
        labValues
      );

      navigation.replace("UploadCompleted");
      return;
    }

    setStatus("Uploading...");

    const timer = setTimeout(() => {
      setStatus("Extracting...");
    }, 1000);

    console.log("Before upload");

    response = await uploadReport(file);

    clearTimeout(timer);

    console.log("=== FULL RESPONSE ===");
    console.log(JSON.stringify(response, null, 2));

      // ✅ Duplicate detected
      if (response.is_duplicate) {
        setDuplicate(true);
        return;
      }
      if (mode !== "confirm") {
        navigation.replace("OCRPreview", {
        tempFileId: response.temp_file_id,

        extractedValues: (response.lab_values || []).map(
        (lab: any, index: number) => ({
        id: String(index + 1),
        testName: lab.test,
        value: String(lab.value),
        unit: lab.unit,
        referenceLow: lab.reference_range?.[0],
        referenceHigh: lab.reference_range?.[1],
        lowConfidence: false,
      })
    ),

    reportTitle: "Lab Report",
  });

  return;
}

navigation.replace("UploadCompleted");
}catch (error: any) {
      console.log("STATUS:", error.response?.status);
      console.log("DATA:", error.response?.data);

      Alert.alert(
        "Upload Failed",
        JSON.stringify(error.response?.data ?? error.message, null, 2)
      );

      navigation.goBack();
    }
  };

  if (duplicate) {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Duplicate Report</Text>

      <Text style={styles.subtitle}>
        This report has already been uploaded.
      </Text>

      <Text
        style={{
          marginTop: 30,
          fontSize: 18,
          fontWeight: "700",
          color: "#2563EB",
        }}
        onPress={() => navigation.goBack()}
      >
        ← Go Back
      </Text>
    </SafeAreaView>
  );
}

  return (
    <SafeAreaView style={styles.container}>
      <ActivityIndicator size="large" color="#2563EB" />

      <Text style={styles.title}>{status}</Text>

      <Text style={styles.subtitle}>
        Please don't close the app.
      </Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
    padding: 24,
  },

  title: {
    marginTop: 30,
    fontSize: 24,
    fontWeight: "700",
    color: "#2563EB",
  },

  subtitle: {
    marginTop: 12,
    color: "#64748B",
    fontSize: 16,
  },
});