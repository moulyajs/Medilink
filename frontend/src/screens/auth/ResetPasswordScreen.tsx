import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

import {
  useNavigation,
  useRoute,
} from "@react-navigation/native";

import { resetPassword } from "../../services/authService";

export default function ResetPasswordScreen() {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();

  const { email, otp } = route.params;

  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleResetPassword = async () => {
    try {
      setLoading(true);

      await resetPassword({
        email,
        otp,
        new_password: newPassword,
      });

      alert("Password changed successfully.");

      navigation.replace("Login");

    } catch (error: any) {
      alert(
        error?.response?.data?.detail ||
        "Password reset failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>

      <Text style={styles.title}>
        Reset Password
      </Text>

      <TextInput
        style={styles.input}
        placeholder="New Password"
        secureTextEntry
        value={newPassword}
        onChangeText={setNewPassword}
      />

      <TouchableOpacity
        style={styles.button}
        onPress={handleResetPassword}
      >
        <Text style={styles.buttonText}>
          {loading ? "Updating..." : "Reset Password"}
        </Text>
      </TouchableOpacity>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
    backgroundColor: "#fff",
  },

  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 32,
    textAlign: "center",
  },

  input: {
    height: 52,
    borderWidth: 1,
    borderColor: "#E2E8F0",
    borderRadius: 12,
    paddingHorizontal: 16,
    marginBottom: 16,
  },

  button: {
    height: 52,
    backgroundColor: "#2563EB",
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },

  buttonText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 16,
  },
});