import React, { useMemo, useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Platform,
} from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

import { TimelineItem } from "../../types/timeline";
import styles from "./styles";

import {
  viewDocument,
  viewDocumentMobile,
} from "../../services/timelineService";

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

export default function TimelineHeader({
  timeline,
}: Props) {
  const [showAll, setShowAll] = useState(false);

  const [openingDocument, setOpeningDocument] =
    useState<string | null>(null);

  const visibleTimeline = useMemo(() => {
    return showAll
      ? timeline
      : timeline.slice(0, 3);
  }, [timeline, showAll]);

  // ==========================================================
  // VIEW DOCUMENT
  // ==========================================================

  const handleViewDocument = async (
    documentId: string
  ) => {
    if (!documentId) {
      alert("Document not found");
      return;
    }

    try {
      console.log(
        "================================"
      );

      console.log(
        "VIEW DOCUMENT"
      );

      console.log(
        "DOCUMENT ID:",
        documentId
      );

      console.log(
        "PLATFORM:",
        Platform.OS
      );

      console.log(
        "================================"
      );

      setOpeningDocument(documentId);

      // ======================================================
      // WEB
      // ======================================================

      if (Platform.OS === "web") {
        const blobUrl =
          await viewDocument(
            documentId
          );

        console.log(
          "Opening authenticated document"
        );

        window.open(
          blobUrl,
          "_blank"
        );

        setTimeout(() => {
          URL.revokeObjectURL(
            blobUrl
          );
        }, 60000);

        return;
      }

      // ======================================================
      // MOBILE
      // ======================================================

      console.log(
        "Opening document on mobile..."
      );

      await viewDocumentMobile(
        documentId
      );

    } catch (error: any) {

      console.error(
        "================================"
      );

      console.error(
        "DOCUMENT VIEW ERROR"
      );

      console.error(
        "ERROR:",
        error
      );

      console.error(
        "MESSAGE:",
        error?.message
      );

      console.error(
        "RESPONSE:",
        error?.response
      );

      console.error(
        "STATUS:",
        error?.response?.status
      );

      console.error(
        "DATA:",
        error?.response?.data
      );

      console.error(
        "================================"
      );

      alert(
        error?.response?.data?.detail ||
        error?.message ||
        "Unable to open medical report."
      );

    } finally {

      setOpeningDocument(null);

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
        contentContainerStyle={
          styles.scrollContent
        }
      >

        {visibleTimeline.map(
          (item, index) => {

            const event =
              getEvent(
                item.document_type
              );

            const isOpening =
              openingDocument ===
              item.source_document;

            return (
              <React.Fragment
                key={item.id}
              >

                <View
                  style={styles.eventItem}
                >

                  {/* Event Icon */}
                  <TouchableOpacity
                    style={[
                      styles.circle,
                      {
                        backgroundColor:
                          event.color,
                      },
                    ]}
                  >

                    <MaterialCommunityIcons
                      name={
                        event.icon as any
                      }
                      size={24}
                      color="#FFFFFF"
                    />

                  </TouchableOpacity>

                  {/* Event Type */}
                  <Text
                    style={styles.eventLabel}
                  >
                    {event.label}
                  </Text>

                  {/* Event Date */}
                  <Text
                    style={styles.eventDate}
                  >
                    {new Date(
                      item.event_date
                    ).toLocaleDateString()}
                  </Text>

                  {/* View Button */}
                  <TouchableOpacity
                    style={
                      styles.viewButton
                    }
                    disabled={isOpening}
                    onPress={() =>
                      handleViewDocument(
                        item.source_document
                      )
                    }
                  >

                    <Text
                      style={
                        styles.viewText
                      }
                    >
                      {isOpening
                        ? "Opening..."
                        : "View"}
                    </Text>

                  </TouchableOpacity>

                </View>

                {/* Connecting Line */}
                {index !==
                  visibleTimeline.length -
                    1 && (
                  <View
                    style={styles.line}
                  />
                )}

              </React.Fragment>
            );
          }
        )}

        {/* Load More */}
        {!showAll &&
          timeline.length > 3 && (
            <>

              <View
                style={styles.line}
              />

              <TouchableOpacity
                style={
                  styles.eventItem
                }
                onPress={() =>
                  setShowAll(true)
                }
              >

                <View
                  style={[
                    styles.circle,
                    {
                      backgroundColor:
                        "#2563EB",
                    },
                  ]}
                >

                  <MaterialCommunityIcons
                    name="chevron-right"
                    size={24}
                    color="#FFFFFF"
                  />

                </View>

                <Text
                  style={
                    styles.eventLabel
                  }
                >
                  Load More
                </Text>

                <Text
                  style={
                    styles.eventDate
                  }
                >
                  +
                  {timeline.length - 3}{" "}
                  Records
                </Text>

              </TouchableOpacity>

            </>
          )}

      </ScrollView>

    </View>
  );
}