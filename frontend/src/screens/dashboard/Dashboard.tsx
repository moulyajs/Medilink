import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { useStyles } from "../../hooks/useStyles";

export default function Dashboard() {
  const navigation = useNavigation<any>();
  const { colors, globalStyles } = useStyles();

  return (
    <View
      style={[
        globalStyles.screen,
        styles.container,
      ]}
    >
      <Text
        style={[
          styles.title,
          { color: colors.primary },
        ]}
      >
        Medilink Dashboard
      </Text>

      <TouchableOpacity
        style={[
          styles.button,
          { backgroundColor: colors.primary },
        ]}
        onPress={() => navigation.navigate("Profile")}
      >
        <Text style={styles.buttonText}>
          Profile
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[
          styles.button,
          { backgroundColor: colors.primary },
        ]}
        onPress={() => navigation.navigate("ChatHome")}
      >
        <Text style={styles.buttonText}>
          Chat Home
        </Text>
      </TouchableOpacity>
      <TouchableOpacity
  style={styles.button}
  onPress={() => navigation.navigate("UploadReport")}
>
  <Text style={styles.buttonText}>
    Upload Report
  </Text>
</TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },

  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 40,
  },

  button: {
    width: "100%",
    height: 52,
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