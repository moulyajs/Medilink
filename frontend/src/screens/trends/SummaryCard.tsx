import React from "react";
import { View, Text, StyleSheet } from "react-native";

interface SummaryCardProps {
  title: string;
  value: string;
}

export default function SummaryCard({
  title,
  value,
}: SummaryCardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>

      <Text style={styles.value}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    width: "48%",

    backgroundColor: "#FFFFFF",

    marginHorizontal: 8,

    minHeight: 110,

    borderRadius: 16,

    padding: 16,

    shadowColor: "#000",

    shadowOpacity: 0.08,

    shadowRadius: 6,

    shadowOffset: {
      width: 0,
      height: 3,
    },

    elevation: 3,
  },

  title: {
    fontSize: 14,

    color: "#64748B",

    marginBottom: 8,

    fontWeight: "500",
  },

  value: {
    fontSize: 24,

    color: "#2563EB",

    fontWeight: "700",
  },
});