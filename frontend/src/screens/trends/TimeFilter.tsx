import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

interface Props {
  selected: string;
  onChange: (value: string) => void;
}

const filters = ["3M", "6M", "1Y", "All"];

export default function TimeFilter({
  selected,
  onChange,
}: Props) {
  return (
    <View style={styles.container}>
      {filters.map((item) => (
        <TouchableOpacity
          key={item}
          style={[
            styles.button,
            selected === item && styles.activeButton,
          ]}
          onPress={() => onChange(item)}
        >
          <Text
            style={[
              styles.text,
              selected === item && styles.activeText,
            ]}
          >
            {item}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "center",
    marginBottom: 24,
  },

  button: {
    width: 70,
    height: 42,
    marginHorizontal: 8,
    borderRadius: 12,

    borderWidth: 1,
    borderColor: "#2563EB",

    justifyContent: "center",
    alignItems: "center",

    backgroundColor: "#FFFFFF",
  },

  activeButton: {
    backgroundColor: "#2563EB",
  },

  text: {
    color: "#2563EB",
    fontWeight: "600",
  },

  activeText: {
    color: "#FFFFFF",
  },
});