import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
} from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

import { TimelineItem } from "../../types/timeline";
import styles from "./styles";

interface Props {
  item: TimelineItem;
}

function getIcon(type: string) {
  switch (type.toUpperCase()) {
    case "LAB_REPORT":
    case "LAB REPORT":
      return {
        icon: "test-tube",
        color: "#2563EB",
      };

    case "PRESCRIPTION":
      return {
        icon: "pill",
        color: "#14B8A6",
      };

    case "ECG":
      return {
        icon: "heart-pulse",
        color: "#22C55E",
      };

    case "DISCHARGE_SUMMARY":
    case "DISCHARGE SUMMARY":
      return {
        icon: "file-document",
        color: "#F59E0B",
      };

    default:
      return {
        icon: "file-document-outline",
        color: "#64748B",
      };
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export default function TimelineCard({ item }: Props) {
  const report = getIcon(item.document_type);

  return (
    <View style={styles.card}>

      <View style={styles.cardHeader}>

        <View
          style={[
            styles.iconBox,
            {
              backgroundColor: report.color,
            },
          ]}
        >
          <MaterialCommunityIcons
            name={report.icon as any}
            size={24}
            color="#FFFFFF"
          />
        </View>

        <View style={styles.headerText}>

          <Text style={styles.cardTitle}>
            {item.document_type.replace(/_/g, " ")}
          </Text>

          <View style={styles.dateBadge}>

            <MaterialCommunityIcons
              name="calendar-month"
              size={15}
              color="#2563EB"
            />

            <Text style={styles.date}>
              {formatDate(item.event_date)}
            </Text>

          </View>

        </View>

      </View>

      <Text style={styles.summary}>
        {item.summary || "Medical record available"}
      </Text>

      <TouchableOpacity
        style={styles.button}
        activeOpacity={0.8}
        onPress={() => {
          // Navigate to Details Screen later
        }}
      >
        <Text style={styles.buttonText}>
          View Details
        </Text>

        <MaterialCommunityIcons
          name="chevron-right"
          size={20}
          color="#2563EB"
        />

      </TouchableOpacity>

    </View>
  );
}