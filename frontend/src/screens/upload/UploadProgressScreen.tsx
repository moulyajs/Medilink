import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useRoute, useNavigation } from "@react-navigation/native";
import { Alert } from "react-native";
import { uploadReport } from "../../services/reportService";

export default function UploadProgressScreen() {
  const route = useRoute<any>();
  const navigation = useNavigation<any>();

  const { file } = route.params;

  const [status, setStatus] = useState("Uploading...");

  useEffect(() => {
    startUpload();
  }, []);

  const startUpload = async () => {
  try {
    setStatus("Uploading...");

    // Show "Extracting..." after a short delay so the user sees both states
    const timer = setTimeout(() => {
      setStatus("Extracting...");
    }, 1000);

    const response = await uploadReport(file);

    clearTimeout(timer);

    console.log(response);

    navigation.replace("UploadCompleted");

  } catch (error: any) {
  console.log("STATUS:", error.response?.status);
  console.log("DATA:", error.response?.data);

  Alert.alert(
    "Upload Failed",
    JSON.stringify(error.response?.data, null, 2)
  );

    navigation.goBack();
  }
};

  return (
    <SafeAreaView style={styles.container}>
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

const styles = StyleSheet.create({
  container:{
    flex:1,
    justifyContent:"center",
    alignItems:"center",
    backgroundColor:"#fff",
    padding:24
  },

  title:{
    marginTop:30,
    fontSize:24,
    fontWeight:"700",
    color:"#2563EB"
  },

  subtitle:{
    marginTop:12,
    color:"#64748B",
    fontSize:16
  }
});