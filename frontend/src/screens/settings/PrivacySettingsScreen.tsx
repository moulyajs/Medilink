import React, { useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import SettingsItem from "../../components/settings/SettingsItem";

export default function PrivacySettingsScreen() {
  const navigation = useNavigation<any>();

  const [biometric, setBiometric] = useState(false);
  const [pinLock, setPinLock] = useState(true);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}

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

        {/* Authentication */}

        <Text style={styles.sectionTitle}>
          Authentication
        </Text>

        <SettingsItem
          icon="finger-print-outline"
          title="Biometric Login"
          subtitle="Use fingerprint or Face ID"
          showSwitch
          switchValue={biometric}
          onSwitchChange={setBiometric}
        />

        <SettingsItem
          icon="key-outline"
          title="PIN Lock"
          subtitle="Require PIN before opening Medilink"
          showSwitch
          switchValue={pinLock}
          onSwitchChange={setPinLock}
        />

        {/* Devices */}

        <Text style={styles.sectionTitle}>
          Devices
        </Text>

        <SettingsItem
          icon="phone-portrait-outline"
          title="Connected Devices"
          subtitle="Manage trusted devices"
        />

        <SettingsItem
          icon="desktop-outline"
          title="Session Management"
          subtitle="View active sessions"
        />

        {/* Data */}

        <Text style={styles.sectionTitle}>
          Privacy
        </Text>

        <SettingsItem
          icon="lock-closed-outline"
          title="Data Encryption"
          subtitle="Your records are end-to-end encrypted"
          showArrow={false}
        />

        <SettingsItem
          icon="shield-outline"
          title="Permissions"
          subtitle="Manage app permissions"
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