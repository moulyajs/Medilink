import React from "react";
import {
  TouchableOpacity,
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../theme/ThemeContext";

type Props = {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  subtitle?: string;
  danger?: boolean;
  onPress: () => void;
};

export default function SettingsItem({
  icon,
  title,
  subtitle,
  danger = false,
  onPress,
}: Props) {

  const { colors, darkMode } = useTheme();

  return (

    <TouchableOpacity
      activeOpacity={0.85}
      style={[
        styles.container,
        {
          backgroundColor: colors.card,
          borderColor: darkMode ? "#374151" : "#E2E8F0",
          shadowColor: colors.text,
        },
      ]}
      onPress={onPress}
    >

      {/* Left Side */}

      <View style={styles.leftContainer}>

        <View
          style={[
            styles.iconContainer,
            {
              backgroundColor: danger
                ? "#FEE2E2"
                : darkMode
                ? "#2D3748"
                : "#EFF6FF",
            },
          ]}
        >

          <Ionicons
            name={icon}
            size={22}
            color={danger ? colors.danger : colors.primary}
          />

        </View>

        <View style={styles.textContainer}>

          <Text
            style={[
              styles.title,
              {
                color: danger
                  ? colors.danger
                  : colors.text,
              },
            ]}
          >
            {title}
          </Text>

          {subtitle && (
            <Text
              style={[
                styles.subtitle,
                {
                  color: colors.subText,
                },
              ]}
            >
              {subtitle}
            </Text>
          )}

        </View>

      </View>

      {/* Arrow */}

      <Ionicons
        name="chevron-forward"
        size={22}
        color={colors.subText}
      />

    </TouchableOpacity>

  );

}

const styles = StyleSheet.create({

  container: {

    flexDirection: "row",

    justifyContent: "space-between",

    alignItems: "center",

    padding: 18,

    borderRadius: 16,

    marginBottom: 16,

    borderWidth: 1,

    shadowOpacity: 0.05,

    shadowRadius: 10,

    shadowOffset: {
      width: 0,
      height: 5,
    },

    elevation: 4,

  },

  leftContainer: {

    flexDirection: "row",

    alignItems: "center",

    flex: 1,

  },

  iconContainer: {

    width: 48,

    height: 48,

    borderRadius: 14,

    justifyContent: "center",

    alignItems: "center",

    marginRight: 16,

  },

  textContainer: {

    flex: 1,

  },

  title: {

    fontSize: 16,

    fontWeight: "600",

  },

  subtitle: {

    marginTop: 4,

    fontSize: 13,

  },

});