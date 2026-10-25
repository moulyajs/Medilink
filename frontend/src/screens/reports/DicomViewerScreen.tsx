import React, { useState } from "react";
import {
  View,
  Text,
  Image,
  Pressable,
  ActivityIndicator,
  ScrollView,
  StyleSheet,
  Alert,
} from "react-native";
import * as DocumentPicker from "expo-document-picker";
import api from "../../services/api";

type DicomMetadata = {
  patient_name?: string;
  patient_id?: string;
  modality?: string;
  study_date?: string;
  study_description?: string;
  rows?: number | string;
  columns?: number | string;
  number_of_frames?: number | string;
};

export default function DicomViewerScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<DicomMetadata | null>(null);
  const [loading, setLoading] = useState(false);

  const selectDicom = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: "*/*",
        copyToCacheDirectory: true,
        multiple: false,
      });

      if (result.canceled || !result.assets?.length) return;

      const file = result.assets[0];

      setLoading(true);
      setImage(null);
      setMetadata(null);

      const formData = new FormData();
      formData.append(
        "file",
        {
          uri: file.uri,
          name: file.name || "scan.dcm",
          type: file.mimeType || "application/dicom",
        } as any
      );

      const response = await api.post("/dicom/view", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setImage(response.data.image);
      setMetadata(response.data.metadata);
    } catch (error: any) {
      console.error("DICOM upload failed:", error?.response?.data || error);

      Alert.alert(
        "DICOM Viewer",
        error?.response?.data?.detail ||
          "Unable to process the DICOM file. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const metadataItem = (label: string, value?: string | number) => (
    <View style={styles.metadataRow} key={label}>
      <Text style={styles.metadataLabel}>{label}</Text>
      <Text style={styles.metadataValue}>
  {value === undefined || value === ""
    ? "Not available"
    : String(value)}
</Text>
    </View>
  );

  function valueNotAvailable(value?: string | number) {
    return value === undefined || value === ""
      ? "Not available"
      : String(value);
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>DICOM Viewer</Text>
      <Text style={styles.subtitle}>
        Upload and preview a medical scan.
      </Text>

      <Pressable
        style={styles.uploadButton}
        onPress={selectDicom}
        disabled={loading}
      >
        <Text style={styles.uploadButtonText}>
          {loading ? "Processing..." : "Select DICOM File"}
        </Text>
      </Pressable>

      {loading && (
        <View style={styles.loading}>
          <ActivityIndicator size="large" color="#147D92" />
          <Text style={styles.subtitle}>Processing your scan...</Text>
        </View>
      )}

      {image && (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Medical Image Preview</Text>
          <Image
            source={{ uri: image }}
            style={styles.scanImage}
            resizeMode="contain"
            accessibilityLabel="DICOM image preview"
          />
        </View>
      )}

      {metadata && (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Scan Metadata</Text>
          {metadataItem("Patient Name", metadata.patient_name)}
          {metadataItem("Patient ID", metadata.patient_id)}
          {metadataItem("Modality", metadata.modality)}
          {metadataItem("Study Date", metadata.study_date)}
          {metadataItem("Study Description", metadata.study_description)}
          {metadataItem("Rows", metadata.rows)}
          {metadataItem("Columns", metadata.columns)}
          {metadataItem("Number of Frames", metadata.number_of_frames)}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: "#F5F7FB",
  },
  title: {
    fontSize: 27,
    fontWeight: "700",
    color: "#173B57",
  },
  subtitle: {
    marginTop: 8,
    marginBottom: 18,
    color: "#64748B",
    fontSize: 14,
  },
  uploadButton: {
    backgroundColor: "#147D92",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
    marginBottom: 20,
  },
  uploadButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  loading: {
    alignItems: "center",
    padding: 20,
  },
  card: {
    backgroundColor: "#FFFFFF",
    padding: 16,
    borderRadius: 14,
    marginBottom: 18,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#173B57",
    marginBottom: 14,
  },
  scanImage: {
    width: "100%",
    height: 320,
    backgroundColor: "#111827",
    borderRadius: 8,
  },
  metadataRow: {
    paddingVertical: 11,
    borderBottomWidth: 1,
    borderBottomColor: "#E2E8F0",
  },
  metadataLabel: {
    fontSize: 12,
    color: "#64748B",
    marginBottom: 4,
  },
  metadataValue: {
    fontSize: 15,
    color: "#1E293B",
  },
});