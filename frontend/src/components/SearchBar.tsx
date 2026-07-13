import React from "react";
import {
  View,
  TextInput,
  StyleSheet,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

import { Colors } from "../theme";

interface Props {
  value: string;
  onChangeText: (text: string) => void;
}

export default function SearchBar({
  value,
  onChangeText,
}: Props) {
  return (
    <View style={styles.container}>
      <Ionicons
        name="search"
        size={22}
        color={Colors.textSecondary}
      />

      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder="Search conversations..."
        style={styles.input}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",

    backgroundColor: Colors.white,

    borderWidth: 1,

    borderColor: Colors.border,

    borderRadius: 16,

    paddingHorizontal: 18,

    height: 56,
  },

  input: {
    flex: 1,
    marginLeft: 12,
    fontSize: 16,
  },
});