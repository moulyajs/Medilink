import React from "react";
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../theme/ThemeContext";

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
  const { colors, darkMode } = useTheme();

  return (
    <TouchableOpacity
      activeOpacity={0.9}
      onPress={onPress}
      disabled={loading}
    >
      <LinearGradient
        colors={
          darkMode
            ? ["#374151", "#1F2937"]
            : [colors.primary, "#1D4ED8"]
        }
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={[
          styles.button,
          {
            shadowColor: colors.shadow,
          },
        ]}
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