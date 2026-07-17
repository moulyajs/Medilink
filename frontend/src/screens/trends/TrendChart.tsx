import React from "react";
import { View, Text, Dimensions, StyleSheet } from "react-native";
import { LineChart } from "react-native-chart-kit";

interface Props {
  history?: {
    date: string;
    value: number;
  }[];
  trend?: string;
}

const screenWidth = Dimensions.get("window").width - 70;

export default function TrendChart({
  history = [],
}: Props) {

  if (history.length === 0) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Trend Graph</Text>

        <View style={styles.graph}>
          <Text>No historical data available</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Trend Graph</Text>

      <LineChart
        data={{
          labels: history.map(item =>
            item.date.substring(5)
          ),
          datasets: [
            {
              data: history.map(item => item.value),
            },
          ],
        }}
        width={screenWidth}
        height={220}
        yAxisSuffix=""
        bezier
        chartConfig={{
          backgroundColor: "#fff",
          backgroundGradientFrom: "#fff",
          backgroundGradientTo: "#fff",
          decimalPlaces: 1,
          color: (opacity = 1) =>
            `rgba(37,99,235,${opacity})`,
          labelColor: () => "#555",
          propsForDots: {
            r: "4",
          },
        }}
        style={{
          borderRadius: 16,
        }}
      />
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