import React from "react";
import {
  TouchableOpacity,
  Text,
  StyleSheet,
} from "react-native";

import { MaterialCommunityIcons } from "@expo/vector-icons";

import { Colors } from "../theme";

interface Props {
  title: string;
  onPress: () => void;
}

export default function Chip({
  title,
  onPress,
}: Props) {
  return (
    <TouchableOpacity
      style={styles.chip}
      onPress={onPress}
    >
      <MaterialCommunityIcons
        name="lightbulb-outline"
        color={Colors.primary}
        size={18}
      />

      <Text style={styles.text}>
        {title}
      </Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  chip: {
    flexDirection: "row",
    alignItems: "center",

    backgroundColor: "#EFF6FF",

    borderRadius: 24,

    paddingHorizontal: 16,

    paddingVertical: 10,

    margin: 6,
  },

  text: {
    marginLeft: 8,

    color: Colors.primary,

    fontWeight: "600",
  },
});