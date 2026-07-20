import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

interface Props {
  device: string;
  platform: string;
  lastActive: string;
  current: boolean;
  onLogout: () => void;
}

export default function SessionCard({
  device,
  platform,
  lastActive,
  current,
  onLogout,
}: Props) {
  return (
    <View style={styles.card}>

      <View style={{ flex: 1 }}>
        <Text style={styles.device}>
          {device}
        </Text>

        <Text style={styles.info}>
          {platform}
        </Text>

        <Text style={styles.info}>
          Last Active: {lastActive}
        </Text>

        {current && (
          <Text style={styles.current}>
            Current Device
          </Text>
        )}
      </View>

      {!current && (
        <TouchableOpacity
          onPress={onLogout}
        >
          <Text style={styles.logout}>
            Logout
          </Text>
        </TouchableOpacity>
      )}

    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fff",
    marginHorizontal: 20,
    marginVertical: 8,
    padding: 18,
    borderRadius: 14,
    flexDirection: "row",
    alignItems: "center",
  },

  device: {
    fontSize: 17,
    fontWeight: "700",
  },

  info: {
    color: "#64748B",
    marginTop: 4,
  },

  current: {
    marginTop: 8,
    color: "#16A34A",
    fontWeight: "700",
  },

  logout: {
    color: "#EF4444",
    fontWeight: "700",
  },
});