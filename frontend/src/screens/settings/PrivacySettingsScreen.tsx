import React, { useEffect, useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  Alert,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import {
  isPinEnabled,
  disablePin,
} from "../../services/pinService";
import SettingsItem from "../../components/settings/SettingsItem";
import { useNavigation } from "@react-navigation/native";
import {
  isBiometricEnabled,
  isBiometricSupported,
  isBiometricEnrolled,
  authenticateBiometric,
  enableBiometric,
  disableBiometric,
} from "../../services/biometricService";

export default function PrivacySettingsScreen() {
  const navigation = useNavigation<any>();
  const [biometric, setBiometric] = useState(false);

  const [pinLock, setPinLock] = useState(false);

  useEffect(() => {
    loadBiometricStatus();
  }, []);

  const loadBiometricStatus = async () => {

  const enabled =
    await isBiometricEnabled();

  setBiometric(enabled);

  const pinEnabled =
    await isPinEnabled();

  setPinLock(pinEnabled);

};

  const handleBiometricToggle = async (value: boolean) => {

    if (value) {

      const supported = await isBiometricSupported();

      if (!supported) {
        Alert.alert(
          "Not Supported",
          "Your device does not support biometric authentication."
        );
        return;
      }

      const enrolled = await isBiometricEnrolled();

      if (!enrolled) {
        Alert.alert(
          "No Biometrics",
          "Please enroll a fingerprint or Face ID in your device settings."
        );
        return;
      }

      const authenticated =
        await authenticateBiometric();

      if (!authenticated) {
        Alert.alert(
          "Authentication Failed",
          "Unable to verify your identity."
        );
        return;
      }

      await enableBiometric();

      setBiometric(true);

      Alert.alert(
        "Success",
        "Biometric login enabled."
      );

    } else {

      await disableBiometric();

      setBiometric(false);

      Alert.alert(
        "Disabled",
        "Biometric login disabled."
      );

    }

  };

  return (

    <SafeAreaView style={styles.container}>

      <ScrollView
        showsVerticalScrollIndicator={false}
      >

        <LinearGradient
          colors={["#5D9DFF", "#4E89B9", "#2563EB"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.header}
        >

          <View style={styles.headerRow}>

            <Ionicons
              name="shield-checkmark"
              size={34}
              color="#FFFFFF"
            />

            <Text style={styles.headerTitle}>
              Privacy & Security
            </Text>

          </View>

          <Text style={styles.headerSubtitle}>
            Protect your medical account and personal data.
          </Text>

        </LinearGradient>

        <Text style={styles.sectionTitle}>
          Authentication
        </Text>

        <SettingsItem
          icon="finger-print-outline"
          title="Biometric Login"
          subtitle="Use fingerprint or Face ID"
          showSwitch
          switchValue={biometric}
          onSwitchChange={handleBiometricToggle}
        />

        <SettingsItem
  icon="key-outline"
  title="PIN Lock"
  subtitle="Require PIN before opening Medilink"
  showSwitch
  switchValue={pinLock}
  onSwitchChange={async (value) => {

    if (value) {

      navigation.navigate("CreatePin");

    } else {

      await disablePin();

      setPinLock(false);

      Alert.alert(
        "Disabled",
        "PIN Lock disabled."
      );

    }

  }}
/>

        <Text style={styles.sectionTitle}>
          Devices
        </Text>

        <SettingsItem
    icon="phone-portrait-outline"
    title="Connected Devices"
    subtitle="Manage trusted devices"
    onPress={() => navigation.navigate("ConnectedDevices")}
/>

        <Text style={styles.sectionTitle}>
          Privacy
        </Text>

        <SettingsItem
  icon="lock-closed-outline"
  title="Data Encryption"
  subtitle="View encryption status"
  onPress={() =>
    navigation.navigate("EncryptionStatus")
  }
/>

        <SettingsItem
  icon="shield-outline"
  title="Permissions"
  subtitle="Manage Camera, Storage & Notifications"
  onPress={() =>
    navigation.navigate("Permissions")
  }
/>

      </ScrollView>

    </SafeAreaView>

  );

}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: "#F5F8FC",
  },

  header: {
    paddingTop: 28,
    paddingBottom: 45,
    paddingHorizontal: 24,
    borderBottomLeftRadius: 35,
    borderBottomRightRadius: 35,
  },

  headerRow: {
    flexDirection: "row",
    alignItems: "center",
  },

  headerTitle: {
    color: "#FFFFFF",
    fontSize: 28,
    fontWeight: "700",
    marginLeft: 12,
  },

  headerSubtitle: {
    color: "#EAF4FF",
    marginTop: 14,
    fontSize: 15,
    lineHeight: 22,
  },

  sectionTitle: {
    marginTop: 28,
    marginBottom: 12,
    marginLeft: 24,
    fontSize: 18,
    fontWeight: "700",
    color: "#1E293B",
  },

});