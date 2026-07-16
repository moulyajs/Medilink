import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useNavigation } from "@react-navigation/native";

import { forgotPassword } from "../../services/authService";

export default function ForgotPasswordScreen() {
  const navigation = useNavigation<any>();

  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSendOTP = async () => {
    try {
      setLoading(true);

      await forgotPassword({
        email,
      });

      alert("OTP sent successfully.");

      navigation.navigate("VerifyOTP", {
        email,
      });

    } catch (error: any) {
      alert(
        error?.response?.data?.detail ||
        "Failed to send OTP."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Forgot Password
      </Text>

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
      />

      <TouchableOpacity
        style={styles.button}
        onPress={handleSendOTP}
      >
        <Text style={styles.buttonText}>
          {loading ? "Sending..." : "Send OTP"}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.link}>
          Back to Login
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

  link: {
    marginTop: 20,
    textAlign: "center",
    color: "#2563EB",
  },
});