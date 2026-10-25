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
  const [saving, setSaving] = useState(false);

  const [selectedFile, setSelectedFile] =
    useState<DocumentPicker.DocumentPickerAsset | null>(null);

  // Select and process a DICOM file
  const selectDicom = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: "*/*",
        copyToCacheDirectory: true,
        multiple: false,
      });

      if (result.canceled || !result.assets?.length) {
        return;
      }

      const file = result.assets[0];

      // Clear the previous scan and retain the newly selected file
      setImage(null);
      setMetadata(null);
      setSelectedFile(file);
      setLoading(true);

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

      if (!response.data?.success || !response.data?.image) {
        throw new Error("The server did not return a valid DICOM preview.");
      }

      setImage(response.data.image);
      setMetadata(response.data.metadata || {});
    } catch (error: any) {
      console.error(
        "DICOM upload failed:",
        error?.response?.data || error
      );

      // Do not allow saving a file that failed to process
      setSelectedFile(null);
      setImage(null);
      setMetadata(null);

      Alert.alert(
        "DICOM Viewer",
        error?.response?.data?.detail ||
          error?.message ||
          "Unable to process the DICOM file. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  // Save the selected DICOM file to the backend
  const saveDicom = async () => {
    if (!selectedFile || !metadata || !image) {
      Alert.alert(
        "Missing File",
        "Please select and process a DICOM file first."
      );
      return;
    }

    try {
      setSaving(true);

      const formData = new FormData();

      formData.append(
        "file",
        {
          uri: selectedFile.uri,
          name: selectedFile.name || "scan.dcm",
          type: selectedFile.mimeType || "application/dicom",
        } as any
      );

      const response = await api.post("/dicom/save", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data?.success === false) {
        throw new Error(
          response.data?.detail || "The server could not save the DICOM report."
        );
      }

      Alert.alert(
        "Success",
        response.data?.message || "DICOM report saved successfully."
      );
    } catch (error: any) {
      console.error(
        "DICOM save failed:",
        error?.response?.data || error
      );

      Alert.alert(
        "Save Failed",
        error?.response?.data?.detail ||
          error?.message ||
          "Unable to save the DICOM report."
      );
    } finally {
      setSaving(false);
    }
  };

  // Display metadata rows
  const metadataItem = (
    label: string,
    value?: string | number
  ) => (
    <View style={styles.metadataRow} key={label}>
      <Text style={styles.metadataLabel}>{label}</Text>
      <Text style={styles.metadataValue}>
        {value === undefined || value === ""
          ? "Not available"
          : String(value)}
      </Text>
    </View>
  );

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>DICOM Viewer</Text>

      <Text style={styles.subtitle}>
        Upload and preview a medical scan.
      </Text>

      <Pressable
        style={[
          styles.uploadButton,
          loading && styles.disabledButton,
        ]}
        onPress={selectDicom}
        disabled={loading || saving}
      >
        <Text style={styles.uploadButtonText}>
          {loading ? "Processing..." : "Select DICOM File"}
        </Text>
      </Pressable>

      {loading && (
        <View style={styles.loading}>
          <ActivityIndicator size="large" color="#147D92" />
          <Text style={styles.subtitle}>
            Processing your scan...
          </Text>
        </View>
      )}

      {image && (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>
            Medical Image Preview
          </Text>

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
          <Text style={styles.sectionTitle}>
            Scan Metadata
          </Text>

          {metadataItem("Patient Name", metadata.patient_name)}
          {metadataItem("Patient ID", metadata.patient_id)}
          {metadataItem("Modality", metadata.modality)}
          {metadataItem("Study Date", metadata.study_date)}
          {metadataItem(
            "Study Description",
            metadata.study_description
          )}
          {metadataItem("Rows", metadata.rows)}
          {metadataItem("Columns", metadata.columns)}
          {metadataItem(
            "Number of Frames",
            metadata.number_of_frames
          )}
        </View>
      )}

      {image && metadata && selectedFile && (
        <Pressable
          style={[
            styles.uploadButton,
            styles.saveButton,
            (saving || loading) && styles.disabledButton,
          ]}
          onPress={saveDicom}
          disabled={saving || loading}
        >
          {saving ? (
            <View style={styles.savingContent}>
              <ActivityIndicator color="#FFFFFF" />
              <Text style={styles.uploadButtonText}>
                Saving Scan...
              </Text>
            </View>
          ) : (
            <Text style={styles.uploadButtonText}>
              Submit DICOM Report
            </Text>
          )}
        </Pressable>
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
    justifyContent: "center",
    marginBottom: 20,
  },
  saveButton: {
    backgroundColor: "#16A34A",
  },
  disabledButton: {
    opacity: 0.6,
  },
  uploadButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  savingContent: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
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