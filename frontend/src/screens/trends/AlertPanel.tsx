import React from "react";
import { View, Text, StyleSheet } from "react-native";

interface Props {
  status: string;
}

export default function AlertPanel({ status }: Props) {

  let backgroundColor = "#22C55E";
  let title = "Healthy";
  let message = "All selected lab values are within the expected trend.";

  if (status === "HIGH") {
    backgroundColor = "#EF4444";
    title = "High Value";
    message =
      "The selected lab test is above the normal reference range.";
  }

  if (status === "LOW") {
    backgroundColor = "#F59E0B";
    title = "Low Value";
    message =
      "The selected lab test is below the normal reference range.";
  }

  return (
    <View style={styles.card}>
      <Text style={styles.heading}>Alerts</Text>

      <View
        style={[
          styles.alertBox,
          {
            backgroundColor,
          },
        ]}
      >
        <Text style={styles.alertTitle}>
          {title}
        </Text>

        <Text style={styles.alertText}>
          {message}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({

  card: {

    backgroundColor: "#FFFFFF",

    borderRadius: 16,

    padding: 16,

    marginBottom: 20,

    shadowColor: "#000",

    shadowOpacity: 0.08,

    shadowRadius: 6,

    elevation: 3,

  },

  heading: {

    fontSize: 18,

    fontWeight: "600",

    color: "#0F172A",

    marginBottom: 16,

  },

  alertBox: {

    borderRadius: 12,

    padding: 16,

  },

  alertTitle: {

    color: "#FFFFFF",

    fontSize: 18,

    fontWeight: "700",

    marginBottom: 8,

  },

  alertText: {

    color: "#FFFFFF",

    fontSize: 15,

    lineHeight: 22,

  },

});