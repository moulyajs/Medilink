import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

type Props = {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  value: string;
};

export default function InfoCard({
  icon,
  title,
  value,
}: Props) {
  return (

    <View style={styles.card}>

      <View style={styles.iconContainer}>

        <Ionicons
          name={icon}
          size={22}
          color="#2563EB"
        />

      </View>

      <View style={styles.textContainer}>

        <Text style={styles.title}>
          {title}
        </Text>

        <Text style={styles.value}>
          {value}
        </Text>

      </View>

    </View>

  );
}

const styles = StyleSheet.create({

  card: {
    flexDirection: "row",
    alignItems: "center",

    backgroundColor: "#FFFFFF",

    padding: 18,

    borderRadius: 16,

    marginBottom: 16,

    borderWidth: 1,
    borderColor: "#E2E8F0",

    shadowColor: "#000",
    shadowOpacity: 0.06,
    shadowRadius: 10,
    shadowOffset: {
      width: 0,
      height: 4,
    },

    elevation: 4,
  },

  iconContainer: {

    width: 48,
    height: 48,

    borderRadius: 12,

    backgroundColor: "#EFF6FF",

    justifyContent: "center",
    alignItems: "center",

    marginRight: 16,

  },

  textContainer: {
    flex: 1,
  },

  title: {
    fontSize: 13,
    color: "#64748B",
    marginBottom: 4,
  },

  value: {
    fontSize: 17,
    fontWeight: "600",
    color: "#0F172A",
  },

});