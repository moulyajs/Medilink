import React from "react";
import { View, Text, StyleSheet } from "react-native";

interface Props {
  trend: string;
  delta: number;
  status: string;
}

export default function KeyInsights({
  trend,
  delta,
  status,
}: Props) {

  let insight = "";

  if (status === "HIGH") {
    insight =
      "This test is above the normal range. Please consult your physician if this trend continues.";
  } else if (status === "LOW") {
    insight =
      "This test is below the normal range. Regular monitoring is recommended.";
  } else {
    insight =
      "This test is currently within the normal range.";
  }

  return (
    <View style={styles.card}>
      <Text style={styles.heading}>
        Key Insights
      </Text>

      <View style={styles.row}>
        <Text style={styles.icon}>📈</Text>
        <Text style={styles.text}>
          Trend: {trend}
        </Text>
      </View>

      <View style={styles.row}>
        <Text style={styles.icon}>📊</Text>
        <Text style={styles.text}>
          Overall Change: {delta}
        </Text>
      </View>

      <View style={styles.row}>
        <Text style={styles.icon}>💡</Text>
        <Text style={styles.text}>
          {insight}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({

  card: {

    backgroundColor:"#FFFFFF",

    borderRadius:16,

    padding:16,

    marginBottom:20,

    elevation:3

  },

  heading:{

    fontSize:18,

    fontWeight:"600",

    marginBottom:16,

    color:"#0F172A"

  },

  row:{

    flexDirection:"row",

    marginBottom:12,

    alignItems:"flex-start"

  },

  icon:{

    fontSize:18,

    marginRight:10

  },

  text:{

    flex:1,

    fontSize:15,

    color:"#334155",

    lineHeight:22

  }

});