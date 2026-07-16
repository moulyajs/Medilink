import React from "react";
import {
  View,
  StyleSheet,
  ViewStyle,
} from "react-native";

import { Colors, Spacing } from "../theme";

interface Props {
  children: React.ReactNode;
  style?: ViewStyle;
}

export default function Card({
  children,
  style,
}: Props) {
  return (
    <View style={[styles.card, style]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.card,

    borderRadius: 20,

    padding: Spacing.md,

    borderWidth: 1,

    borderColor: Colors.border,

    shadowColor: "#000",

    shadowOpacity: 0.12,

    shadowRadius: 8,

    shadowOffset: {
      width: 0,
      height: 4,
    },

    elevation: 6,
  },
});