import React from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import { useTheme } from "../../theme/ThemeContext";

export default function EncryptionStatusScreen() {
  const navigation = useNavigation<any>();
  const { colors, darkMode } = useTheme();

  const SecurityItem = ({
    title,
    subtitle,
  }: {
    title: string;
    subtitle: string;
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
          name="shield-checkmark"
          size={28}
          color={colors.success}
        />

        <View style={{ marginLeft: 15, flex: 1 }}>
          <Text
            style={[
              styles.title,
              { color: colors.text },
            ]}
          >
            {title}
          </Text>

          <Text
            style={[
              styles.subtitle,
              { color: colors.subText },
            ]}
          >
            {subtitle}
          </Text>
        </View>

        <Ionicons
          name="checkmark-circle"
          size={24}
          color={colors.success}
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
            Data Encryption
          </Text>

          <Text style={styles.headerSubtitle}>
            Your medical data is securely protected
          </Text>
        </LinearGradient>

        <View style={styles.content}>
          <SecurityItem
            title="AES-256 Encryption"
            subtitle="All medical reports are encrypted using AES-256."
          />

          <SecurityItem
            title="Secure HTTPS"
            subtitle="All communication uses HTTPS/TLS encryption."
          />

          <SecurityItem
            title="Encrypted Cloud Storage"
            subtitle="Uploaded records remain encrypted in storage."
          />

          <SecurityItem
            title="Secure Authentication"
            subtitle="PIN and Biometric authentication are supported."
          />

          <SecurityItem
            title="Protected AI Chat"
            subtitle="Chat communication is securely transmitted."
          />

          <SecurityItem
            title="Privacy Protection"
            subtitle="Your personal information is never shared."
          />
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

  title: {
    fontSize: 17,
    fontWeight: "700",
  },

  subtitle: {
    marginTop: 5,
    fontSize: 14,
    lineHeight: 20,
  },
});