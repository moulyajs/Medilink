import React, { useEffect, useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  ScrollView,
  ActivityIndicator
} from "react-native";

import SummaryCard from "./SummaryCard";
import TrendDropdown from "./TrendDropdown";
import TrendChart from "./TrendChart";
import AlertPanel from "./AlertPanel";
import TimeFilter from "./TimeFilter";
import KeyInsights from "./KeyInsights";
import { styles } from "./styles";

import { getTrendAnalysis } from "../../services/trendService";
import { TrendData } from "../../types/trend";


const PATIENT_ID = "fcc28785-edbb-4398-aa82-ad453de58ad2";

export default function TrendScreen() {

  const [loading, setLoading] = useState(true);

  const [trendData, setTrendData] = useState<TrendData[]>([]);

  const [selectedTest, setSelectedTest] = useState("");

  const [selectedFilter, setSelectedFilter] = useState("3M");

  useEffect(() => {

    loadTrend();

  }, []);

  async function loadTrend() {

    setLoading(true);

    const data = await getTrendAnalysis(PATIENT_ID);

    setTrendData(data);

    if (data.length > 0)
        setSelectedTest(data[0].test_name);

    setLoading(false);
  }

  const selected =
    trendData.find(t => t.test_name === selectedTest);

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

        <Text style={styles.heading}>

          Trend Analysis

        </Text>

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
            value={String(selected?.latest_value ?? "-")}
          />

        </View>

        <View style={styles.cardRow}>

          <SummaryCard
            title="Overall Change"
            value={String(selected?.delta ?? "-")}
          />

          <SummaryCard
            title="Data Points"
            value={String(selected?.data_points ?? "-")}
          />

        </View>

        <TrendDropdown
          data={trendData}
          selected={selectedTest}
          onChange={setSelectedTest}
        />

        <TrendChart
          history={selected?.history ?? []}
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

