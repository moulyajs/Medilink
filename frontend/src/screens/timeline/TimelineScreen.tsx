import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  ActivityIndicator,
} from "react-native";

import TimelineHeader from "../../components/timeline/TimelineHeader";
import styles from "./styles";

import { TimelineItem } from "../../types/timeline";
import { getTimeline } from "../../services/timelineService";

export default function TimelineScreen() {

  const [timeline, setTimeline] = useState<TimelineItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTimeline();
  }, []);

async function loadTimeline() {
  try {

    const data = await getTimeline();

    console.log("Timeline:", data);

    setTimeline(data);

  } catch (err) {
    console.log(err);
  } finally {
    setLoading(false);
  }
}

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator
          size="large"
          color="#2563EB"
        />
      </View>
    );
  }

  return (
    <View style={styles.container}>

      <Text style={styles.title}>
        Medical Timeline
      </Text>

      {timeline.length === 0 ? (

        <View style={styles.loadingContainer}>
          <Text
            style={{
              color: "#64748B",
              fontSize: 16,
            }}
          >
            No Medical Records Found
          </Text>
        </View>

      ) : (

        <TimelineHeader
          timeline={timeline}
        />

      )}

    </View>
  );
}