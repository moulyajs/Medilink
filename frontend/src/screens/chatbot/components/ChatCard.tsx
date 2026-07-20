import React from "react";
import {
  TouchableOpacity,
  View,
  Text,
  StyleSheet,
} from "react-native";

import Card from "../../../components/Card";
import { Colors } from "../../../theme";
import { Ionicons } from "@expo/vector-icons";

interface Props {
  title: string;
  description: string;
  date: string;
  onPress: () => void;
  onDelete: () => void;
}

export default function ChatCard({
  title,
  description,
  date,
  onPress,
  onDelete,
}: Props) {
  return (
    <TouchableOpacity
      activeOpacity={0.8}
      onPress={onPress}
    >
      <Card style={styles.card}>
       <View style={styles.row}>
  <View style={styles.content}>
    <Text style={styles.title}>{title}</Text>

    {!!description && (
      <Text style={styles.description}>
        {description}
      </Text>
    )}
  </View>

  <View style={styles.rightSection}>
    <Text style={styles.date}>
      {date}
    </Text>

    <TouchableOpacity
      onPress={onDelete}
      style={styles.deleteButton}
    >
      <Ionicons
        name="trash-outline"
        size={22}
        color="#E53935"
      />
    </TouchableOpacity>
  </View>
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
  justifyContent: "space-between",
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
  content: {
  flex: 1,
},

rightSection: {
  alignItems: "flex-end",
  justifyContent: "space-between",
  height: 50,
},

deleteButton: {
  marginTop: 8,
},
});