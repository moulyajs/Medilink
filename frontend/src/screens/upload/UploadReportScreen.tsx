import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import * as ImagePicker from "expo-image-picker";
import * as DocumentPicker from "expo-document-picker";
import { Alert } from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function UploadReportScreen() {
    const navigation = useNavigation<any>();
    const openCamera = async () => {
  const permission =
    await ImagePicker.requestCameraPermissionsAsync();

  if (!permission.granted) {
    Alert.alert(
      "Permission Required",
      "Camera permission is required."
    );
    return;
  }

  const result =
    await ImagePicker.launchCameraAsync({
      mediaTypes: ["images"],
      quality: 1,
    });

  if (!result.canceled) {
    navigation.navigate("UploadProgress", {
    file: result.assets[0],
});
  }
};
const pickPDF = async () => {
  const result =
    await DocumentPicker.getDocumentAsync({
      type: "application/pdf",
      copyToCacheDirectory: true,
    });

  if (!result.canceled) {
    navigation.navigate("UploadProgress", {
    file: result.assets[0],
});
  }
};
const openGallery = async () => {
  const permission =
    await ImagePicker.requestMediaLibraryPermissionsAsync();

  if (!permission.granted) {
    Alert.alert(
      "Permission Required",
      "Gallery permission is required."
    );
    return;
  }

  const result =
    await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      quality: 1,
    });

  if (!result.canceled) {
    const asset = result.assets[0];

    console.log("Gallery asset:", asset);

    navigation.navigate("UploadProgress", {
      file: asset,
    });
  }
};
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Upload Report</Text>

      <TouchableOpacity
  style={styles.option}
  onPress={openCamera}
>
  <Ionicons
    name="camera-outline"
    size={28}
    color="#2563EB"
  />
  <Text style={styles.optionText}>Camera</Text>
</TouchableOpacity>

      <TouchableOpacity
  style={styles.option}
  onPress={openGallery}
>
  <Ionicons
    name="images-outline"
    size={28}
    color="#2563EB"
  />
  <Text style={styles.optionText}>Gallery</Text>
</TouchableOpacity>

      <TouchableOpacity
  style={styles.option}
  onPress={pickPDF}
>
  <Ionicons
    name="document-text-outline"
    size={28}
    color="#2563EB"
  />
  <Text style={styles.optionText}>PDF</Text>
</TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8FAFC",
    padding: 24,
  },

  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#0F172A",
    marginBottom: 32,
  },

  option: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 20,
    marginBottom: 18,
    elevation: 2,
  },

  optionText: {
    fontSize: 18,
    marginLeft: 18,
    color: "#0F172A",
    fontWeight: "600",
  },
});