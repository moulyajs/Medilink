import React, { useMemo, useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Linking,
  Platform,
} from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

import { TimelineItem } from "../../types/timeline";
import styles from "./styles";

interface Props {
  timeline: TimelineItem[];
}

function getEvent(type: string) {
  switch (type.toUpperCase()) {
    case "LAB REPORT":
    case "LAB_REPORT":
      return {
        icon: "test-tube",
        color: "#2563EB",
        label: "Lab",
      };

    case "DISCHARGE SUMMARY":
    case "DISCHARGE_SUMMARY":
      return {
        icon: "file-document",
        color: "#F59E0B",
        label: "Discharge",
      };

    case "PRESCRIPTION":
      return {
        icon: "pill",
        color: "#14B8A6",
        label: "Medicine",
      };

    case "ECG":
      return {
        icon: "heart-pulse",
        color: "#EF4444",
        label: "ECG",
      };

    case "SCAN":
      return {
        icon: "image",
        color: "#8B5CF6",
        label: "Scan",
      };

    default:
      return {
        icon: "file-document-outline",
        color: "#64748B",
        label: "Record",
      };
  }
}

export default function TimelineHeader({ timeline }: Props) {
  const [showAll, setShowAll] = useState(false);

  const visibleTimeline = useMemo(() => {
    return showAll ? timeline : timeline.slice(0, 3);
  }, [timeline, showAll]);

  // View uploaded PDF
  const viewDocument = (documentId: string) => {
    if (!documentId) {
      alert("Document not found");
      return;
    }

    const url = `http://127.0.0.1:8000/document/${documentId}`;

    console.log("Opening:", url);

    if (Platform.OS === "web") {
      window.open(url, "_blank");
    } else {
      Linking.openURL(url);
    }
  };

  return (
    <View style={styles.timelineContainer}>
      <Text style={styles.timelineTitle}>
        Patient Medical Journey
      </Text>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {visibleTimeline.map((item, index) => {
          const event = getEvent(item.document_type);

          return (
            <React.Fragment key={item.id}>
              <View style={styles.eventItem}>
                <TouchableOpacity
                  style={[
                    styles.circle,
                    {
                      backgroundColor: event.color,
                    },
                  ]}
                >
                  <MaterialCommunityIcons
                    name={event.icon as any}
                    size={24}
                    color="#FFFFFF"
                  />
                </TouchableOpacity>

                <Text style={styles.eventLabel}>
                  {event.label}
                </Text>

                <Text style={styles.eventDate}>
                  {new Date(item.event_date).toLocaleDateString()}
                </Text>

                <TouchableOpacity
                  style={styles.viewButton}
                  onPress={() =>
                    viewDocument(item.source_document)
                  }
                >
                  <Text style={styles.viewText}>
                    View
                  </Text>
                </TouchableOpacity>
              </View>

              {index !== visibleTimeline.length - 1 && (
                <View style={styles.line} />
              )}
            </React.Fragment>
          );
        })}

        {!showAll && timeline.length > 3 && (
          <>
            <View style={styles.line} />

            <TouchableOpacity
              style={styles.eventItem}
              onPress={() => setShowAll(true)}
            >
              <View
                style={[
                  styles.circle,
                  {
                    backgroundColor: "#2563EB",
                  },
                ]}
              >
                <MaterialCommunityIcons
                  name="chevron-right"
                  size={24}
                  color="#FFFFFF"
                />
              </View>

              <Text style={styles.eventLabel}>
                Load More
              </Text>

              <Text style={styles.eventDate}>
                +{timeline.length - 3} Records
              </Text>
            </TouchableOpacity>
          </>
        )}
      </ScrollView>
    </View>
  );
}