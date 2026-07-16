import React from "react";
import {
  View,
  Text,
 StyleSheet,
} from "react-native";

import { Colors } from "../theme";

interface Props {
  letter?: string;
}

export default function Avatar({
  letter = "AI",
}: Props) {
  return (
    <View style={styles.avatar}>
      <Text style={styles.text}>
        {letter}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  avatar: {
    width: 42,

    height: 42,

    borderRadius: 21,

    backgroundColor: Colors.primary,

    justifyContent: "center",

    alignItems: "center",
  },

  text: {
    color: Colors.white,

    fontWeight: "700",
  },
});