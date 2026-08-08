import React from "react";
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  KeyboardTypeOptions,
} from "react-native";

type Props = {
  label: string;
  placeholder: string;
  value: string;
  onChangeText?: (text: string) => void;
  editable?: boolean;
  keyboardType?: KeyboardTypeOptions;
  multiline?: boolean;
  icon?: string; // Optional for compatibility if you're passing it
};

export default function CustomInput({
  label,
  placeholder,
  value,
  onChangeText,
  editable = true,
  keyboardType = "default",
  multiline = false,
}: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>

      <TextInput
        style={[
          styles.input,
          multiline && styles.multilineInput,
          !editable && styles.disabledInput,
        ]}
        placeholder={placeholder}
        value={value}
        onChangeText={onChangeText}
        editable={editable}
        keyboardType={keyboardType}
        multiline={multiline}
        textAlignVertical={multiline ? "top" : "center"}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 18,
  },

  label: {
    marginBottom: 8,
    fontWeight: "600",
    fontSize: 15,
    color: "#334155",
  },

  input: {
    height: 54,
    borderWidth: 1,
    borderColor: "#CBD5E1",
    borderRadius: 14,
    paddingHorizontal: 16,
    fontSize: 16,
    backgroundColor: "#FFFFFF",
  },

  multilineInput: {
    height: 100,
    paddingTop: 16,
  },

  disabledInput: {
    backgroundColor: "#F1F5F9",
    color: "#64748B",
  },
});