import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Switch,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../theme/ThemeContext";

type Props = {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  subtitle?: string;

  onPress?: () => void;

  showArrow?: boolean;

  showSwitch?: boolean;

  switchValue?: boolean;

  onSwitchChange?: (value: boolean) => void;

  danger?: boolean;
};

export default function SettingsItem({
  icon,
  title,
  subtitle,
  onPress,
  showArrow = true,
  showSwitch = false,
  switchValue = false,
  onSwitchChange,
  danger = false,
}: Props) {
  const { colors } = useTheme();

  return (
    <TouchableOpacity
      activeOpacity={0.8}
      onPress={onPress}
      disabled={showSwitch}
      style={[
        styles.container,
        {
          backgroundColor: colors.card,
          shadowColor: colors.text,
        },
      ]}
    >
      {/* Left */}

      <View style={styles.leftSection}>
        <View
          style={[
            styles.iconContainer,
            {
              backgroundColor: danger
                ? "#FEE2E2"
                : colors.primary + "20",
            },
          ]}
        >
          <Ionicons
            name={icon}
            size={22}
            color={danger ? "#DC2626" : colors.primary}
          />
        </View>

        <View style={styles.textContainer}>
          <Text
            style={[
              styles.title,
              {
                color: danger ? "#DC2626" : colors.text,
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
                  color: colors.text,
                },
              ]}
            >
              {subtitle}
            </Text>
          )}
        </View>
      </View>

      {/* Right */}

      {showSwitch ? (
        <Switch
          value={switchValue}
          onValueChange={onSwitchChange}
          trackColor={{
            false: "#CBD5E1",
            true: colors.primary,
          }}
          thumbColor="#FFFFFF"
        />
      ) : (
        showArrow && (
          <Ionicons
            name="chevron-forward"
            size={22}
            color={colors.text}
          />
        )
      )}
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",

    padding: 18,
    borderRadius: 18,
    marginBottom: 14,

    shadowOpacity: 0.05,
    shadowRadius: 12,
    shadowOffset: {
      width: 0,
      height: 4,
    },

    elevation: 4,
  },

  leftSection: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
  },

  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,

    justifyContent: "center",
    alignItems: "center",
  },

  textContainer: {
    marginLeft: 16,
    flex: 1,
  },

  title: {
    fontSize: 16,
    fontWeight: "700",
  },

  subtitle: {
    marginTop: 4,
    fontSize: 13,
  },
});