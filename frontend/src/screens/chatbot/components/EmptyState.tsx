import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Colors } from "../../../theme";

export default function EmptyState() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        No conversations yet
      </Text>

      <Text style={styles.subtitle}>
        Start a new conversation with Medilink AI.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    padding: 40,
  },

  title: {
    fontSize: 18,
    fontWeight: "600",
    color: Colors.text,
  },

  subtitle: {
    marginTop: 8,
    color: Colors.textSecondary,
    textAlign: "center",
  },
});