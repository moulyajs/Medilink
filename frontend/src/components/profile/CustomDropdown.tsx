import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

type Props = {
  label: string;
  value: string;
  placeholder: string;
  onPress: () => void;
};

export default function CustomDropdown({

  label,

  value,

  placeholder,

  onPress,

}: Props) {

  return (

    <View style={styles.container}>

      <Text style={styles.label}>
        {label}
      </Text>

      <TouchableOpacity
        activeOpacity={0.8}
        style={styles.dropdown}
        onPress={onPress}
      >

        <Text
          style={[
            styles.value,
            !value && styles.placeholder,
          ]}
        >
          {value || placeholder}
        </Text>

        <Ionicons
          name="chevron-down"
          size={22}
          color="#64748B"
        />

      </TouchableOpacity>

    </View>

  );

}

const styles = StyleSheet.create({

  container: {
    marginBottom: 18,
  },

  label: {
    fontSize: 15,
    fontWeight: "600",
    color: "#334155",
    marginBottom: 8,
  },

  dropdown: {

    height: 56,

    borderRadius: 16,

    borderWidth: 1,

    borderColor: "#CBD5E1",

    backgroundColor: "#FFFFFF",

    flexDirection: "row",

    justifyContent: "space-between",

    alignItems: "center",

    paddingHorizontal: 18,

    shadowColor: "#000",

    shadowOpacity: 0.03,

    shadowRadius: 6,

    elevation: 2,

  },

  value: {

    fontSize: 16,

    color: "#0F172A",

  },

  placeholder: {

    color: "#94A3B8",

  },

});