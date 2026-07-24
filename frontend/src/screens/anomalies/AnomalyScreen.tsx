import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  StyleSheet,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { Ionicons } from "@expo/vector-icons";
import { TouchableOpacity } from "react-native";

import { getAnomalies, Anomaly } from "../../services/anomalyService";

const AnomalyScreen = () => {
  const [loading, setLoading] = useState(true);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const navigation = useNavigation<any>();
  useEffect(() => {
    loadAnomalies();
  }, []);

  const loadAnomalies = async () => {
    try {
      const data = await getAnomalies();
      setAnomalies(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <ActivityIndicator
        size="large"
        style={{ marginTop: 40 }}
      />
    );
  }

  if (anomalies.length === 0) {
    return (
      <View style={styles.center}>
        <Text>No personalized anomalies detected.</Text>
      </View>
    );
  }

return (
  <View style={{ flex: 1 }}>
    <View style={styles.header}>
      <TouchableOpacity onPress={() => navigation.goBack()}>
        <Ionicons
          name="arrow-back"
          size={26}
          color="#2563EB"
        />
      </TouchableOpacity>

      <Text style={styles.headerTitle}>
        Personal Baseline & Anomalies
      </Text>
    </View>

    <FlatList
      data={anomalies}
      keyExtractor={(item) => item.test_name}
      renderItem={({ item }) => (
  <View style={styles.card}>
    <View style={styles.cardHeader}>
      <View>
        <Text style={styles.title}>{item.test_name}</Text>
        <Text style={styles.subtitle}>
          Personalized anomaly detected
        </Text>
      </View>

      <View style={styles.badge}>
        <Text style={styles.badgeText}>ALERT</Text>
      </View>
    </View>

    <View style={styles.divider} />

    <View style={styles.row}>
      <Text style={styles.label}>Current Value</Text>
      <Text style={styles.value}>
        {item.current_value} {item.unit}
      </Text>
    </View>

    <View style={styles.row}>
      <Text style={styles.label}>Clinical Range</Text>
      <Text style={styles.value}>
        {item.reference_low} - {item.reference_high} {item.unit}
      </Text>
    </View>

    <View style={styles.row}>
      <Text style={styles.label}>Personal Average</Text>
      <Text style={styles.value}>
        {item.personal_average} {item.unit}
      </Text>
    </View>

    <View style={styles.row}>
      <Text style={styles.label}>Personal Range</Text>
      <Text style={styles.value}>
        {item.personal_min} - {item.personal_max} {item.unit}
      </Text>
    </View>

    <View style={styles.divider} />

    <View style={styles.metricsContainer}>
      <View style={styles.metric}>
        <Text style={styles.metricTitle}>Deviation</Text>
        <Text style={styles.metricValue}>
          {item.deviation > 0 ? "+" : ""}
          {item.deviation}
        </Text>
      </View>

      <View style={styles.metric}>
        <Text style={styles.metricTitle}>Change</Text>
        <Text
          style={[
            styles.metricValue,
            {
              color:
                item.percent_change < 0
                  ? "#DC2626"
                  : "#16A34A",
            },
          ]}
        >
          {item.percent_change > 0 ? "↑" : "↓"}{" "}
          {Math.abs(item.percent_change).toFixed(1)}%
        </Text>
      </View>

      <View style={styles.metric}>
        <Text style={styles.metricTitle}>Trend</Text>
        <Text style={styles.metricValue}>
          {item.trend}
        </Text>
      </View>
    </View>

    <View style={styles.infoBox}>
      <Ionicons
        name="information-circle-outline"
        size={18}
        color="#2563EB"
      />

      <Text style={styles.infoText}>
        This result is different from your usual values, so it has been highlighted.
      </Text>
    </View>

    <Text style={styles.footer}>
      Based on {item.sample_count} previous reports
    </Text>
  </View>
)}
    />
  </View>
);
};

export default AnomalyScreen;

const styles = StyleSheet.create({
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },

  card: {
  backgroundColor: "#FFFFFF",
  borderRadius: 18,
  marginHorizontal: 16,
  marginTop: 16,
  padding: 18,
  elevation: 4,
},

cardHeader: {
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
},

title: {
  fontSize: 21,
  fontWeight: "700",
  color: "#111827",
},

subtitle: {
  color: "#6B7280",
  marginTop: 2,
  fontSize: 13,
},

badge: {
  backgroundColor: "#FEE2E2",
  paddingHorizontal: 10,
  paddingVertical: 6,
  borderRadius: 20,
},

badgeText: {
  color: "#DC2626",
  fontWeight: "700",
  fontSize: 12,
},

divider: {
  height: 1,
  backgroundColor: "#E5E7EB",
  marginVertical: 16,
},

row: {
  flexDirection: "row",
  justifyContent: "space-between",
  marginBottom: 12,
},

label: {
  fontSize: 15,
  color: "#6B7280",
},

value: {
  fontSize: 15,
  fontWeight: "600",
  color: "#111827",
},

metricsContainer: {
  flexDirection: "row",
  justifyContent: "space-between",
  marginTop: 10,
},

metric: {
  alignItems: "center",
  flex: 1,
},

metricTitle: {
  fontSize: 13,
  color: "#6B7280",
},

metricValue: {
  marginTop: 4,
  fontSize: 17,
  fontWeight: "700",
  color: "#111827",
},

infoBox: {
  flexDirection: "row",
  backgroundColor: "#EFF6FF",
  padding: 12,
  borderRadius: 12,
  marginTop: 18,
},

infoText: {
  flex: 1,
  marginLeft: 8,
  color: "#1E3A8A",
  fontSize: 14,
},

footer: {
  marginTop: 18,
  textAlign: "center",
  color: "#6B7280",
  fontSize: 13,
},
  header: {
  flexDirection: "row",
  alignItems: "center",
  paddingHorizontal: 16,
  paddingVertical: 16,
  backgroundColor: "#FFFFFF",
  elevation: 2,
},

headerTitle: {
  fontSize: 20,
  fontWeight: "700",
  marginLeft: 16,
  color: "#2563EB",
},
});