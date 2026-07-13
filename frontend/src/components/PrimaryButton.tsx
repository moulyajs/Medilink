import React from "react";
import {
  TouchableOpacity,
  Text,
  StyleSheet,
} from "react-native";

import { Colors, Spacing } from "../theme";

interface Props {
  title: string;
  onPress: () => void;
}

export default function PrimaryButton({
  title,
  onPress,
}: Props) {
  return (
    <TouchableOpacity
      style={styles.button}
      onPress={onPress}
      activeOpacity={0.85}
    >
      <Text style={styles.text}>
        {title}
      </Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: Colors.primary,

    height: 52,

    borderRadius: 12,

    justifyContent: "center",

    alignItems: "center",
  },

  text: {
    color: Colors.white,

    fontSize: 16,

    fontWeight: "600",
  },
});