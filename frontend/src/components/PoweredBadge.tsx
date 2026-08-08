import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

export default function PoweredBadge() {

  return (

    <View style={styles.badge}>

      <Ionicons
        name="sparkles"
        size={16}
        color="#4E89F9"
      />

      <Text style={styles.text}>
        POWERED BY AI
      </Text>

    </View>

  );

}

const styles = StyleSheet.create({

  badge: {

    alignSelf: "center",

    flexDirection: "row",

    alignItems: "center",

    backgroundColor: "#EEF5FF",

    borderRadius: 20,

    paddingHorizontal: 18,

    paddingVertical: 8,

    borderWidth: 1,

    borderColor: "#D5E7FF",

  },

  text: {

    marginLeft: 8,

    color: "#4E89F9",

    fontWeight: "700",

    letterSpacing: 1,

    fontSize: 12,

  },

});