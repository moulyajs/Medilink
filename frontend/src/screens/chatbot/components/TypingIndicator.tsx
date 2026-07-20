import React from "react";
import {
  View,
  StyleSheet,
} from "react-native";

import { Colors, Spacing } from "../../../theme";

export default function TypingIndicator() {
  return (
    <View style={styles.container}>
      <View style={styles.dot} />
      <View style={styles.dot} />
      <View style={styles.dot} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignSelf: "flex-start",

    flexDirection: "row",

    backgroundColor: Colors.botBubble,

    borderRadius: 18,

    padding: Spacing.md,

    marginVertical: 8,
  },

  dot: {
    width: 8,
    height: 8,

    borderRadius: 4,

    backgroundColor: Colors.primary,

    marginHorizontal: 3,
  },
});