import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import {
  authenticateBiometric,
  isBiometricEnabled,
} from "../../services/biometricService";
import { useNavigation } from "@react-navigation/native";
// import { registerForPushNotifications } from "../../services/notificationService";
import { saveToken } from "../../utils/storage";
import { login } from "../../services/authService";
import { getToken } from "../../utils/storage";
import * as Device from "expo-device";
import { Platform } from "react-native";
export default function LoginScreen() {
  const navigation = useNavigation<any>();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const checkBiometric = async () => {

  try {

    const token = await getToken();

    if (!token) return;

    const enabled = await isBiometricEnabled();

    if (!enabled) return;

    const authenticated = await authenticateBiometric();

    if (authenticated) {
      navigation.replace("Dashboard");
    }

  } catch (error) {
    console.log(error);
  }
};
useEffect(() => {
  checkBiometric();
}, []);
  const handleLogin = async () => {
    try {
      setLoading(true);
console.log({
  device_name: Device.modelName,
  device_os: `${Device.osName} ${Device.osVersion}`,
  device_type: Device.deviceType,
});
console.log("DEVICE INFO");
console.log(Device.modelName);
console.log(Device.osName);
console.log(Device.osVersion);
console.log(Device.deviceType);
      const response = await login({
  email,
  password,

  device_name: Device.modelName,

  device_os: `${Device.osName} ${Device.osVersion}`,

  device_type: Device.deviceType
    ? Device.deviceType.toString()
    : "Unknown",
});

      await saveToken(response.data.access_token);
      // const pushToken =
      // await registerForPushNotifications();

      // console.log(pushToken);
      alert("Login Successful!");

      navigation.replace("Dashboard");
    } catch (error: any) {
      alert(
        error?.response?.data?.detail ||
          "Invalid email or password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Welcome Back
      </Text>

      <TextInput
        placeholder="Email"
        style={styles.input}
        value={email}
        onChangeText={setEmail}
      />

      <TextInput
        placeholder="Password"
        style={styles.input}
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TouchableOpacity
        style={styles.button}
        onPress={handleLogin}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? "Logging In..." : "Login"}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        onPress={() =>
          navigation.navigate("Signup")
        }
      >
        <Text style={styles.link}>
          Don't have an account? Sign Up
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        onPress={() =>
          navigation.navigate("ForgotPassword")
        }
      >
        <Text style={styles.link}>
          Forgot Password?
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
    color: "white",
    fontSize: 16,
    fontWeight: "600",
  },

  link: {
    marginTop: 20,
    color: "#2563EB",
    textAlign: "center",
  },
});