import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import FloatingGlow from "./FloatingGlow";

export default function TimelineCard({
  title,
  subtitle,
  date,
  icon,
}: any) {
  return (
    <View style={styles.wrapper}>
      {/* Left Timeline */}

      <View style={styles.leftSide}>

        <FloatingGlow>
          <View style={styles.iconCircle}>
            <Ionicons
              name={icon || "medkit"}
              size={24}
              color="#FFFFFF"
            />
          </View>
        </FloatingGlow>

        <View style={styles.verticalLine} />

      </View>

      {/* Right Card */}

      <View style={styles.card}>

        <View style={styles.header}>

          <View>

            <Text style={styles.title}>
              {title}
            </Text>

            <Text style={styles.sub}>
              {subtitle}
            </Text>

          </View>

          <View style={styles.date}>
            <Text style={styles.day}>{date}</Text>
          </View>

        </View>

        {/* Pills */}

        <View style={styles.pills}>

          <View style={styles.pill}>
            <Ionicons
              name="person"
              size={12}
              color="#6F92AA"
            />

            <Text style={styles.pillText}>
              Dr. Sharma
            </Text>
          </View>

          <View style={styles.pill}>
            <Ionicons
              name="time"
              size={12}
              color="#6F92AA"
            />

            <Text style={styles.pillText}>
              10:30 AM
            </Text>
          </View>

        </View>

        {/* Description */}

        <View style={styles.noteBox}>

          <Text style={styles.note}>
            Routine follow-up. Blood work ordered.
          </Text>

        </View>

      </View>

    </View>
  );
}

const styles = StyleSheet.create({

  wrapper: {
    flexDirection: "row",
    marginBottom: 28,
  },

  leftSide: {
    width: 70,
    alignItems: "center",
  },

  iconCircle: {
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: "#4E89B9",

    justifyContent: "center",
    alignItems: "center",

    shadowColor: "#4E89B9",
    shadowOpacity: 0.35,
    shadowRadius: 14,

    elevation: 8,
  },

  verticalLine: {
    flex: 1,
    width: 2,
    marginTop: 6,
    backgroundColor: "#CFE5F5",
    borderStyle: "dashed",
  },

  card: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    borderRadius: 22,
    padding: 18,

    shadowColor: "#000",
    shadowOpacity: 0.08,
    shadowRadius: 12,

    elevation: 6,
  },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  title: {
    fontSize: 18,
    fontWeight: "700",
    color: "#264B68",
  },

  sub: {
    marginTop: 4,
    color: "#7E98AF",
    fontSize: 13,
  },

  date: {
    width: 56,
    height: 56,
    borderRadius: 18,
    backgroundColor: "#EDF6FC",

    justifyContent: "center",
    alignItems: "center",
  },

  day: {
    color: "#4E89B9",
    fontWeight: "700",
  },

  pills: {
    flexDirection: "row",
    marginTop: 16,
  },

  pill: {
    flexDirection: "row",
    alignItems: "center",

    backgroundColor: "#F3F8FC",

    paddingHorizontal: 10,
    paddingVertical: 6,

    borderRadius: 20,
    marginRight: 10,
  },

  pillText: {
    marginLeft: 5,
    color: "#6E8FA7",
    fontSize: 11,
  },

  noteBox: {
    marginTop: 18,
    backgroundColor: "#F7FBFE",
    borderRadius: 14,
    padding: 12,
    borderWidth: 1,
    borderColor: "#E3EEF7",
  },

  note: {
    color: "#6C8CA5",
    fontSize: 13,
    lineHeight: 18,
  },

});