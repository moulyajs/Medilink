import React from "react";
import {
  View,
  Text,
  StyleSheet,
} from "react-native";
import { Picker } from "@react-native-picker/picker";

import { TrendData } from "../../types/trend";

interface Props {
  data: TrendData[];
  selected: string;
  onChange: (value: string) => void;
}

export default function TrendDropdown({
  data,
  selected,
  onChange,
}: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>
        Select Test
      </Text>

      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={selected}
          onValueChange={(itemValue) =>
            onChange(itemValue)
          }
        >
          {data.map((item) => (
            <Picker.Item
              key={item.test_name}
              label={item.test_name}
              value={item.test_name}
            />
          ))}
        </Picker>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 20,
  },

  label: {
    fontSize: 18,
    fontWeight: "600",
    color: "#0F172A",
    marginBottom: 8,
  },

  pickerContainer: {
    backgroundColor: "#FFFFFF",

    borderWidth: 1,

    borderColor: "#E2E8F0",

    borderRadius: 12,

    overflow: "hidden",
  },
});