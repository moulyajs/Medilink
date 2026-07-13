import React from "react";
import {
  TouchableOpacity,
  View,
  Text,
  StyleSheet,
} from "react-native";

import Card from "../../../components/Card";
import { Colors } from "../../../theme";

interface Props {
  title: string;
  description: string;
  date: string;
  onPress: () => void;
}

export default function ChatCard({
  title,
  description,
  date,
  onPress,
}: Props) {
  return (
    <TouchableOpacity
      activeOpacity={0.8}
      onPress={onPress}
    >
      <Card style={styles.card}>
        <View style={styles.row}>
          <View style={{ flex: 1 }}>
            <Text style={styles.title}>
              {title}
            </Text>

            <Text style={styles.description}>
              {description}
            </Text>
          </View>

          <Text style={styles.date}>
            {date}
          </Text>
        </View>
      </Card>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    marginBottom: 16,
  },

  row: {
    flexDirection: "row",
    alignItems: "center",
  },

  title: {
    fontSize: 18,
    fontWeight: "600",
    color: Colors.text,
  },

  description: {
    marginTop: 6,
    color: Colors.textSecondary,
  },

  date: {
    color: Colors.primary,
    fontWeight: "600",
  },
});