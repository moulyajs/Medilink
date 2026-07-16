import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Switch,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

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
  return (
    <TouchableOpacity
      activeOpacity={0.8}
      style={styles.container}
      onPress={onPress}
      disabled={showSwitch}
    >
      {/* Left */}

      <View style={styles.leftSection}>

        <View
          style={[
            styles.iconContainer,
            danger && styles.dangerIcon,
          ]}
        >
          <Ionicons
            name={icon}
            size={22}
            color={danger ? "#DC2626" : "#2563EB"}
          />
        </View>

        <View style={styles.textContainer}>

          <Text
            style={[
              styles.title,
              danger && styles.dangerText,
            ]}
          >
            {title}
          </Text>

          {subtitle && (
            <Text style={styles.subtitle}>
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
            true: "#60A5FA",
          }}
          thumbColor="#FFFFFF"
        />
      ) : (
        showArrow && (
          <Ionicons
            name="chevron-forward"
            size={22}
            color="#94A3B8"
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

    backgroundColor: "#FFFFFF",

    padding: 18,

    borderRadius: 18,

    marginBottom: 14,

    shadowColor: "#000",

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

    backgroundColor: "#EFF6FF",

    justifyContent: "center",

    alignItems: "center",
  },

  dangerIcon: {

    backgroundColor: "#FEE2E2",
  },

  textContainer: {

    marginLeft: 16,

    flex: 1,
  },

  title: {

    fontSize: 16,

    fontWeight: "700",

    color: "#0F172A",
  },

  subtitle: {

    marginTop: 4,

    color: "#64748B",

    fontSize: 13,
  },

  dangerText: {

    color: "#DC2626",
  },

});