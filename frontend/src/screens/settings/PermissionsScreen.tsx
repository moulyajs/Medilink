import React, { useEffect, useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Linking,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import { useTheme } from "../../theme/ThemeContext";

import * as ImagePicker from "expo-image-picker";

export default function PermissionsScreen() {
  const navigation = useNavigation<any>();
  const { colors, darkMode } = useTheme();

  const [camera, setCamera] = useState("Checking...");
  const [storage, setStorage] = useState("Checking...");

  useEffect(() => {
    loadPermissions();
  }, []);

  const loadPermissions = async () => {
    try {
      // Camera Permission
      let cameraPermission =
        await ImagePicker.getCameraPermissionsAsync();

      if (!cameraPermission.granted && cameraPermission.canAskAgain) {
        cameraPermission =
          await ImagePicker.requestCameraPermissionsAsync();
      }

      setCamera(cameraPermission.granted ? "Granted" : "Denied");

      // Media Library Permission
      let storagePermission =
        await ImagePicker.getMediaLibraryPermissionsAsync();

      if (
        !storagePermission.granted &&
        storagePermission.canAskAgain
      ) {
        storagePermission =
          await ImagePicker.requestMediaLibraryPermissionsAsync();
      }

      setStorage(storagePermission.granted ? "Granted" : "Denied");

      console.log("Camera:", cameraPermission);
      console.log("Storage:", storagePermission);
    } catch (error) {
      console.log(error);
    }
  };

  const PermissionCard = ({
    icon,
    title,
    status,
  }: {
    icon: keyof typeof Ionicons.glyphMap;
    title: string;
    status: string;
  }) => (
    <View
      style={[
        styles.card,
        {
          backgroundColor: colors.card,
          borderColor: colors.border,
        },
      ]}
    >
      <View style={styles.row}>
        <Ionicons
          name={icon}
          size={28}
          color={colors.primary}
        />

        <View style={{ flex: 1, marginLeft: 15 }}>
          <Text
            style={[
              styles.permissionTitle,
              {
                color: colors.text,
              },
            ]}
          >
            {title}
          </Text>

          <Text
            style={[
              styles.status,
              {
                color:
                  status === "Granted"
                    ? colors.success
                    : colors.danger,
              },
            ]}
          >
            {status}
          </Text>
        </View>

        <Ionicons
          name={
            status === "Granted"
              ? "checkmark-circle"
              : "close-circle"
          }
          size={26}
          color={
            status === "Granted"
              ? colors.success
              : colors.danger
          }
        />
      </View>
    </View>
  );

  return (
    <SafeAreaView
      style={[
        styles.container,
        {
          backgroundColor: colors.background,
        },
      ]}
    >
      <ScrollView showsVerticalScrollIndicator={false}>
        <LinearGradient
          colors={
            darkMode
              ? ["#1E293B", "#111827", "#000000"]
              : ["#5D9DFF", "#4E89B9", "#2563EB"]
          }
          style={styles.header}
        >
          <TouchableOpacity
            onPress={() => navigation.goBack()}
          >
            <Ionicons
              name="arrow-back"
              size={24}
              color="#FFF"
            />
          </TouchableOpacity>

          <Text style={styles.headerTitle}>
            Permissions
          </Text>

          <Text style={styles.headerSubtitle}>
            Manage app permissions
          </Text>
        </LinearGradient>

        <View style={styles.content}>
          <PermissionCard
            icon="camera-outline"
            title="Camera"
            status={camera}
          />

          <PermissionCard
            icon="images-outline"
            title="Media Library"
            status={storage}
          />

          <TouchableOpacity
            style={[
              styles.button,
              {
                backgroundColor: colors.primary,
              },
            ]}
            onPress={() => Linking.openSettings()}
          >
            <Ionicons
              name="settings-outline"
              size={20}
              color="#FFF"
            />

            <Text style={styles.buttonText}>
              Open Device Settings
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.refreshButton,
              {
                borderColor: colors.primary,
              },
            ]}
            onPress={loadPermissions}
          >
            <Ionicons
              name="refresh"
              size={20}
              color={colors.primary}
            />

            <Text
              style={[
                styles.refreshText,
                {
                  color: colors.primary,
                },
              ]}
            >
              Refresh Permissions
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  header: {
    paddingTop: 50,
    paddingBottom: 35,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },

  headerTitle: {
    marginTop: 18,
    color: "#FFF",
    fontSize: 28,
    fontWeight: "700",
  },

  headerSubtitle: {
    color: "#EAF4FF",
    marginTop: 8,
    fontSize: 15,
  },

  content: {
    padding: 20,
  },

  card: {
    borderRadius: 18,
    borderWidth: 1,
    padding: 18,
    marginBottom: 18,
  },

  row: {
    flexDirection: "row",
    alignItems: "center",
  },

  permissionTitle: {
    fontSize: 17,
    fontWeight: "700",
  },

  status: {
    marginTop: 5,
    fontSize: 14,
    fontWeight: "600",
  },

  button: {
    height: 55,
    borderRadius: 15,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
    marginTop: 10,
  },

  buttonText: {
    color: "#FFF",
    fontWeight: "700",
    fontSize: 16,
    marginLeft: 10,
  },

  refreshButton: {
    marginTop: 15,
    height: 55,
    borderRadius: 15,
    borderWidth: 1.5,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
  },

  refreshText: {
    fontWeight: "700",
    fontSize: 16,
    marginLeft: 10,
  },
});