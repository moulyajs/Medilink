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
      //console.log("========== SENDING TO BACKEND ==========");
      //console.log(JSON.stringify(labValues, null, 2));
      //console.log("========================================");
      response = await confirmReport(
        tempFileId,
        labValues
      );

      if (response.is_duplicate) {
        Alert.alert(
          "Duplicate Report",
          "This report has already been saved."
        );

        navigation.goBack();
        return;
      }

      navigation.replace("UploadCompleted");
      return;
}

    setStatus("Uploading...");

    const timer = setTimeout(() => {
      setStatus("Extracting...");
  }, 1000);

  try {
    response = await uploadReport(file);
} finally {
    clearTimeout(timer);
}

    //console.log("=== FULL RESPONSE ===");
    //console.log(JSON.stringify(response, null, 2));
    //console.log("UPLOAD RESPONSE:", response);
    //console.log("is_duplicate =", response.is_duplicate);
    //console.log("temp_file_id =", response.temp_file_id);
    //console.log("lab_values length =", response.lab_values?.length);
    

      // ✅ Duplicate detected
      if (response.is_duplicate) {
        //console.log("DUPLICATE DETECTED");
        setDuplicate(true);
        return;
      }
      if (mode !== "confirm") {
        //console.log("ABOUT TO NAVIGATE TO OCRPreview");
        navigation.replace("OCRPreview", {
        tempFileId: response.temp_file_id,

        extractedValues: (response.lab_values || []).map(
        (lab: any, index: number) => ({
        ...lab,                         // ✅ keep everything
            id: String(index + 1),

            // UI fields
            testName: lab.test,
            value: String(lab.value),
            referenceLow: lab.reference_range?.[0],
            referenceHigh: lab.reference_range?.[1],
            lowConfidence: false,
          })
        ),

    reportTitle: "Lab Report",
  });
  
  //console.log("NAVIGATION CALLED");
  return;
}

navigation.replace("UploadCompleted");

}catch (error: any) {
 // console.log("STATUS:", error.response?.status);
  //console.log(
  //"DETAIL:",
  //JSON.stringify(error.response?.data, null, 2)
//);
  //console.error(error);

  Alert.alert(
    "Upload Failed",
    error?.stack || error?.message || JSON.stringify(error, null, 2)
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