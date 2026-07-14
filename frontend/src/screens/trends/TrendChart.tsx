import React from "react";
import { View, Text, StyleSheet } from "react-native";

interface Props {
  history?: any[];
  trend?: string;
}

export default function TrendChart({ history, trend }: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Trend Graph</Text>

      <View style={styles.graph}>
        <Text>Trend graph will be shown here.</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
  },

  title: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 16,
  },

  graph: {
    height: 220,
    backgroundColor: "#F1F5F9",
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },
});