import React from "react";
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

export default function HelpSupportScreen() {
  const navigation = useNavigation<any>();

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
              name="help-circle"
              size={34}
              color="#FFFFFF"
            />

            <Text style={styles.headerTitle}>
              Help & Support
            </Text>
          </View>

          <Text style={styles.headerSubtitle}>
            We're here whenever you need assistance.
          </Text>
        </LinearGradient>

        {/* Help Center */}

        <Text style={styles.sectionTitle}>
          Help Center
        </Text>

        <SettingsItem
          icon="help-circle-outline"
          title="FAQ"
          subtitle="Frequently Asked Questions"
          onPress={() => navigation.navigate("FAQ")}
        />

        <SettingsItem
          icon="mail-outline"
          title="Contact Support"
          subtitle="Reach our support team"
          onPress={() => navigation.navigate("ContactSupport")}
        />

        <SettingsItem
          icon="bug-outline"
          title="Report an Issue"
          subtitle="Help us improve Medilink"
          onPress={() => navigation.navigate("ReportIssue")}
        />

        {/* Legal */}

        <Text style={styles.sectionTitle}>
          Legal
        </Text>

        <SettingsItem
          icon="document-text-outline"
          title="Terms & Conditions"
          subtitle="Read our terms of use"
          onPress={() => navigation.navigate("Terms")}
        />

        <SettingsItem
          icon="shield-checkmark-outline"
          title="Privacy Policy"
          subtitle="Learn how your data is protected"
          onPress={() => navigation.navigate("PrivacyPolicy")}
        />

        {/* Version */}

        <View style={styles.versionCard}>
          <Ionicons
            name="information-circle-outline"
            size={30}
            color="#2563EB"
          />

          <Text style={styles.versionTitle}>
            Medilink
          </Text>

          <Text style={styles.versionText}>
            Version 1.0.0
          </Text>

          <Text style={styles.versionSub}>
            © 2026 Medilink. All Rights Reserved.
          </Text>
        </View>

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
    marginLeft: 12,
    color: "#FFFFFF",
    fontSize: 28,
    fontWeight: "700",
  },

  headerSubtitle: {
    marginTop: 14,
    color: "#EAF4FF",
    fontSize: 15,
  },

  sectionTitle: {
    marginTop: 28,
    marginBottom: 12,
    marginLeft: 24,
    fontSize: 18,
    fontWeight: "700",
    color: "#1E293B",
  },

  versionCard: {
    backgroundColor: "#FFFFFF",
    margin: 24,
    borderRadius: 20,
    padding: 24,
    alignItems: "center",

    shadowColor: "#000",
    shadowOpacity: 0.06,
    shadowRadius: 10,
    shadowOffset: {
      width: 0,
      height: 4,
    },

    elevation: 4,
  },

  versionTitle: {
    marginTop: 12,
    fontSize: 20,
    fontWeight: "700",
    color: "#0F172A",
  },

  versionText: {
    marginTop: 6,
    color: "#64748B",
  },

  versionSub: {
    marginTop: 16,
    textAlign: "center",
    color: "#94A3B8",
    fontSize: 12,
  },
});