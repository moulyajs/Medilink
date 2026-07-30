import React from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import { useTheme } from "../../theme/ThemeContext";

export default function AboutMedilinkScreen() {
  const navigation = useNavigation<any>();
  const { colors, darkMode } = useTheme();

  return (
    <SafeAreaView
      style={[
        styles.container,
        { backgroundColor: colors.background },
      ]}
    >
      {/* Header */}

      <LinearGradient
        colors={
          darkMode
            ? ["#1E293B", "#111827", "#000000"]
            : ["#5D9DFF", "#4E89B9", "#2563EB"]
        }
        style={styles.header}
      >
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons
            name="arrow-back"
            size={24}
            color="#FFFFFF"
          />
        </TouchableOpacity>

        <Text style={styles.headerTitle}>
          About Medilink
        </Text>

        <Text style={styles.headerSubtitle}>
          Smart Healthcare Companion
        </Text>
      </LinearGradient>

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >
        {/* App Card */}

        <View
          style={[
            styles.card,
            {
              backgroundColor: colors.card,
              borderColor: colors.border,
              shadowColor: colors.shadow,
            },
          ]}
        >
          <View
            style={[
              styles.logo,
              {
                backgroundColor: colors.primary,
              },
            ]}
          >
            <Ionicons
              name="medical"
              size={42}
              color="#FFFFFF"
            />
          </View>

          <Text
            style={[
              styles.appName,
              { color: colors.text },
            ]}
          >
            Medilink
          </Text>

          <Text
            style={[
              styles.version,
              { color: colors.subText },
            ]}
          >
            Version 1.0.0
          </Text>
        </View>

        {/* About */}

        <View
          style={[
            styles.card,
            {
              backgroundColor: colors.card,
              borderColor: colors.border,
            },
          ]}
        >
          <Text
            style={[
              styles.sectionTitle,
              { color: colors.primary },
            ]}
          >
            About
          </Text>

          <Text
            style={[
              styles.description,
              { color: colors.subText },
            ]}
          >
            Medilink is an AI-powered healthcare
            application designed to securely manage
            medical records, analyze laboratory
            reports, provide intelligent health
            insights, and simplify patient care
            through modern technology.
          </Text>
        </View>

        {/* Features */}

        <View
          style={[
            styles.card,
            {
              backgroundColor: colors.card,
              borderColor: colors.border,
            },
          ]}
        >
          <Text
            style={[
              styles.sectionTitle,
              { color: colors.primary },
            ]}
          >
            Key Features
          </Text>

          {[
            "AI Health Assistant",
            "Medical Report Upload",
            "OCR Report Extraction",
            "Lab Trend Analysis",
            "Health Timeline",
            "Secure Cloud Storage",
          ].map((item, index) => (
            <View
              key={index}
              style={styles.featureRow}
            >
              <Ionicons
                name="checkmark-circle"
                size={20}
                color={colors.success}
              />

              <Text
                style={[
                  styles.featureText,
                  { color: colors.text },
                ]}
              >
                {item}
              </Text>
            </View>
          ))}
        </View>

        {/* Mission */}

        <View
          style={[
            styles.card,
            {
              backgroundColor: colors.card,
              borderColor: colors.border,
            },
          ]}
        >
          <Text
            style={[
              styles.sectionTitle,
              { color: colors.primary },
            ]}
          >
            Our Mission
          </Text>

          <Text
            style={[
              styles.description,
              { color: colors.subText },
            ]}
          >
            To empower individuals with secure,
            intelligent, and accessible digital
            healthcare solutions that improve
            medical decision-making and promote
            healthier lives.
          </Text>
        </View>

        {/* Footer */}

        <Text
          style={[
            styles.footer,
            { color: colors.subText },
          ]}
        >
          © 2026 Medilink
        </Text>

        <Text
          style={[
            styles.footer,
            {
              color: colors.subText,
              marginTop: 4,
            },
          ]}
        >
          Built with ❤️ for Better Healthcare
        </Text>
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
    color: "#FFFFFF",
    fontSize: 28,
    fontWeight: "700",
    marginTop: 18,
  },

  headerSubtitle: {
    color: "#EAF4FF",
    marginTop: 8,
    fontSize: 15,
  },

  content: {
    padding: 20,
    paddingBottom: 40,
  },

  card: {
    borderRadius: 20,
    padding: 20,
    marginBottom: 18,
    borderWidth: 1,

    shadowOpacity: 0.08,
    shadowRadius: 10,
    shadowOffset: {
      width: 0,
      height: 5,
    },

    elevation: 5,
  },

  logo: {
    width: 90,
    height: 90,
    borderRadius: 45,
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    marginBottom: 15,
  },

  appName: {
    fontSize: 26,
    fontWeight: "700",
    textAlign: "center",
  },

  version: {
    fontSize: 15,
    textAlign: "center",
    marginTop: 6,
  },

  sectionTitle: {
    fontSize: 20,
    fontWeight: "700",
    marginBottom: 12,
  },

  description: {
    fontSize: 15,
    lineHeight: 24,
  },

  featureRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 14,
  },

  featureText: {
    fontSize: 16,
    marginLeft: 12,
  },

  footer: {
    textAlign: "center",
    fontSize: 13,
  },
});