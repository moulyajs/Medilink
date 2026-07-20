import React from "react";
import {
  TouchableOpacity,
  View,
  Text,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

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

  return (

    <TouchableOpacity
      activeOpacity={0.85}
      style={styles.container}
      onPress={onPress}
    >

      {/* Left Side */}

      <View style={styles.leftContainer}>

        <View
          style={[
            styles.iconContainer,
            danger && styles.dangerBackground,
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

      {/* Arrow */}

      <Ionicons
        name="chevron-forward"
        size={22}
        color="#94A3B8"
      />

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

    borderRadius: 16,

    marginBottom: 16,

    borderWidth: 1,

    borderColor: "#E2E8F0",

    shadowColor: "#000",

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

    backgroundColor: "#EFF6FF",

    justifyContent: "center",

    alignItems: "center",

    marginRight: 16,

  },

  dangerBackground: {

    backgroundColor: "#FEE2E2",

  },

  textContainer: {

    flex: 1,

  },

  title: {

    fontSize: 16,

    fontWeight: "600",

    color: "#0F172A",

  },

  subtitle: {

    marginTop: 4,

    fontSize: 13,

    color: "#64748B",

  },

  dangerText: {

    color: "#DC2626",

  },

});