import React from "react";
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";

type Props = {
  title: string;
  onPress: () => void;
  icon?: keyof typeof Ionicons.glyphMap;
  loading?: boolean;
};

export default function PrimaryButton({
  title,
  onPress,
  icon,
  loading = false,
}: Props) {
  return (
    <TouchableOpacity
      activeOpacity={0.9}
      onPress={onPress}
      disabled={loading}
    >
      <LinearGradient
        colors={["#2563EB", "#1D4ED8"]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={styles.button}
      >
        {loading ? (
          <ActivityIndicator color="#FFFFFF" />
        ) : (
          <>
            {icon && (
              <Ionicons
                name={icon}
                size={20}
                color="#FFFFFF"
                style={styles.icon}
              />
            )}

            <Text style={styles.text}>
              {title}
            </Text>
          </>
        )}
      </LinearGradient>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({

  button: {

    height: 54,

    borderRadius: 14,

    justifyContent: "center",
    alignItems: "center",

    flexDirection: "row",

    shadowColor: "#2563EB",

    shadowOpacity: 0.25,

    shadowRadius: 12,

    shadowOffset: {
      width: 0,
      height: 6,
    },

    elevation: 6,

  },

  text: {

    color: "#FFFFFF",

    fontSize: 17,

    fontWeight: "700",

  },

  icon: {

    marginRight: 10,

  },

});