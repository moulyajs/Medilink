import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function Dashboard() {
  const navigation = useNavigation<any>();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Medilink Dashboard</Text>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate("Profile")}
      >
        <Text style={styles.buttonText}>Profile</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate("ChatHome")}
      >
        <Text style={styles.buttonText}>Chat Home</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    padding: 24,
  },

  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 40,
    color: "#2563EB",
  },

  button: {
    width: "100%",
    height: 52,
    backgroundColor: "#2563EB",
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 16,
  },

  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
});