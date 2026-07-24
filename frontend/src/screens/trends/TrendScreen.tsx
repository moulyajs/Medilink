import React, { useEffect, useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  TouchableOpacity,
} from "react-native";

import SummaryCard from "./SummaryCard";
import TrendDropdown from "./TrendDropdown";
import TrendChart from "./TrendChart";
import AlertPanel from "./AlertPanel";
import TimeFilter from "./TimeFilter";
import KeyInsights from "./KeyInsights";
import { styles } from "./styles";
import { useNavigation } from "@react-navigation/native";
import { getTrendAnalysis } from "../../services/trendService";
import { TrendData } from "../../types/trend";
import { Ionicons } from "@expo/vector-icons";

export default function TrendScreen() {
  const navigation = useNavigation<any>();
  const [loading, setLoading] = useState(true);


  const [trendData, setTrendData] = useState<TrendData[]>([]);

  const [selectedTest, setSelectedTest] = useState("");

  const [selectedFilter, setSelectedFilter] = useState("3M");

  useEffect(() => {
    loadTrend();
  }, []);

  async function loadTrend() {
  try {
    setLoading(true);

    

    const data = await getTrendAnalysis();

    setTrendData(data);

    if (data.length > 0) {
      setSelectedTest(data[0].test_name);
    }
  } finally {
    setLoading(false);
  }
}

  const selected = trendData.find(
    (t) => t.test_name === selectedTest
  );

  // -----------------------------
  // Filter History
  // -----------------------------
  const filterHistory = (
    history: { date: string; value: number }[],
    filter: string
  ) => {
    if (!history || history.length === 0) return [];

    if (filter === "ALL") return history;

    const now = new Date();
    const cutoff = new Date(now);

    switch (filter) {
      case "3M":
        cutoff.setMonth(now.getMonth() - 3);
        break;

      case "6M":
        cutoff.setMonth(now.getMonth() - 6);
        break;

      case "1Y":
        cutoff.setFullYear(now.getFullYear() - 1);
        break;

      default:
        return history;
    }

    return history.filter(
      (item) => new Date(item.date) >= cutoff
    );
  };

  const filteredHistory = filterHistory(
    selected?.history ?? [],
    selectedFilter
  );

  // -----------------------------
  // Summary values
  // -----------------------------
  const currentValue =
    filteredHistory.length > 0
      ? filteredHistory[filteredHistory.length - 1].value
      : "-";

  const overallChange =
    filteredHistory.length > 1
      ? (
          filteredHistory[filteredHistory.length - 1].value -
          filteredHistory[0].value
        ).toFixed(2)
      : "-";

  const dataPoints = filteredHistory.length;

  if (loading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator
          size="large"
          color="#2563EB"
        />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
  <TouchableOpacity
    onPress={() => navigation.goBack()}
    style={styles.backButton}
  >
    <Ionicons
      name="arrow-back"
      size={26}
      color="#1E293B"
    />
  </TouchableOpacity>

  <Text style={styles.heading}>
    Trend Analysis
  </Text>
</View>

        <TimeFilter
          selected={selectedFilter}
          onChange={setSelectedFilter}
        />

        <View style={styles.cardRow}>
          <SummaryCard
            title="Trend Status"
            value={selected?.trend ?? "-"}
          />

          <SummaryCard
            title="Current Value"
            value={String(currentValue)}
          />
        </View>

        <View style={styles.cardRow}>
          <SummaryCard
            title="Overall Change"
            value={String(overallChange)}
          />

          <SummaryCard
            title="Data Points"
            value={String(dataPoints)}
          />
        </View>

        <TrendDropdown
          data={trendData}
          selected={selectedTest}
          onChange={setSelectedTest}
        />

        <TrendChart
          history={filteredHistory}
          trend={selected?.trend ?? ""}
        />

        <AlertPanel
          status={selected?.status ?? ""}
        />

        <KeyInsights
          trend={selected?.trend ?? ""}
          delta={selected?.delta ?? 0}
          status={selected?.status ?? ""}
        />
      </ScrollView>
    </SafeAreaView>
  );
}
