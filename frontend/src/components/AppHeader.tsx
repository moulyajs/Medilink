import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

import { Colors, Typography, Spacing } from "../theme";

interface Props {
  title: string;
  subtitle: string;
}

export default function AppHeader({
  title,
  subtitle,
}: Props) {
  return (
    <View style={styles.container}>
      <View style={styles.avatar}>
        <MaterialCommunityIcons
          name="robot-happy-outline"
          size={34}
          color="#fff"
        />
      </View>

      <Text style={styles.title}>
        {title}
      </Text>

      <Text style={styles.subtitle}>
        {subtitle}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    marginVertical: 36,
  },

  avatar: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: Colors.primary,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: Spacing.md,
  },

  title: {
    ...Typography.pageTitle,
    color: Colors.text,
  },

  subtitle: {
    marginTop: 8,
    color: Colors.textSecondary,
    textAlign: "center",
    paddingHorizontal: 30,
    lineHeight: 22,
  },
});