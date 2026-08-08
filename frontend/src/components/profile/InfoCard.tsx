import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../theme/ThemeContext";

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
  const { colors, darkMode } = useTheme();

  return (
    <View
      style={[
        styles.card,
        {
          backgroundColor: colors.card,
          borderColor: colors.border,
          shadowColor: colors.shadow,
        },
      ]}
    >
      <View
        style={[
          styles.iconContainer,
          {
            backgroundColor: darkMode
              ? "#2A2A2A"
              : "#EFF6FF",
          },
        ]}
      >
        <Ionicons
          name={icon}
          size={22}
          color={colors.primary}
        />
      </View>

      <View style={styles.textContainer}>
        <Text
          style={[
            styles.title,
            {
              color: colors.subText,
            },
          ]}
        >
          {title}
        </Text>

        <Text
          style={[
            styles.value,
            {
              color: colors.text,
            },
          ]}
        >
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

    padding: 18,

    borderRadius: 16,

    marginBottom: 16,

    borderWidth: 1,

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

    justifyContent: "center",
    alignItems: "center",

    marginRight: 16,
  },

  textContainer: {
    flex: 1,
  },

  title: {
    fontSize: 13,
    marginBottom: 4,
  },

  value: {
    fontSize: 17,
    fontWeight: "600",
  },
});