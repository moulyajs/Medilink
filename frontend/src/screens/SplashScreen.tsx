import React, { useEffect, useState } from "react";
import { LinearGradient } from "expo-linear-gradient";
import {
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { isPinEnabled } from "../services/pinService";
import AnimatedLogo from "../components/AnimatedLogo";
import api from "../services/api";
import { getToken, removeToken } from "../utils/storage";
import {
  isBiometricEnabled,
  authenticateBiometric,
} from "../services/biometricService";
export default function SplashScreen() {
  const navigation = useNavigation<any>();

  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let value = 0;

    const interval = setInterval(() => {
      value += 2;

      if (value > 100) value = 100;

      setProgress(value);

      if (value >= 100) {
  clearInterval(interval);

  setTimeout(async () => {
  const token = await getToken();
  console.log("TOKEN =", token);

/*
 First app launch
*/
if (!token) {
  console.log("NO TOKEN -> LOGIN");
  navigation.replace("Login");
  return;
}
console.log("JWT VALID");
try {

  /*
   Verify JWT with backend
  */
 console.log("Checking JWT...");
await api.get("/auth/me");
console.log("JWT VALID");
  await api.get("/auth/me");

  /*
   Check if biometric is enabled
  */
  const biometricEnabled =
    await isBiometricEnabled();

if (biometricEnabled) {

    const authenticated =
      await authenticateBiometric();

    if (authenticated) {
       console.log("BIOMETRIC SUCCESS");
      navigation.replace("Dashboard");

      return;

    }

}

const pinEnabled =
    await isPinEnabled();

if (pinEnabled) {
    console.log("PIN LOGIN");
    navigation.replace("PinLogin");

    return;

}
console.log("NORMAL DASHBOARD");
navigation.replace("Dashboard");

} catch {
  console.log("JWT INVALID");
  /*
   Token expired or invalid
  */
  await removeToken();

  navigation.replace("Login");

}
}, 300);
}
    }, 50);

    return () => clearInterval(interval);
  }, []);

  return (
    <LinearGradient
      colors={["#F9FCFF", "#EEF7FC", "#F9FCFF"]}
      style={styles.gradient}
    >
      <View style={styles.phone}>
        <SafeAreaView style={styles.container}>

          <View style={styles.circle1} />
          <View style={styles.circle2} />
          <View style={styles.circle3} />

          {/* Version */}

          <View style={styles.versionContainer}>
            <Text style={styles.version}>
              V2.4.1 • CLINICAL SUITE
            </Text>
          </View>

          {/* Logo */}

          <AnimatedLogo />

          {/* Title */}

          <Text style={styles.title}>
            Medilink
          </Text>

          {/* Subtitle */}

          <View style={styles.subtitleRow}>

            <View style={styles.line} />

            <Text style={styles.subtitle}>
              MEDICAL DATA PLATFORM
            </Text>

            <View style={styles.line} />

          </View>

          {/* Card */}

          <View style={styles.infoCard}>

            <Text style={styles.infoTitle}>
              Precision health data,
            </Text>

            <Text style={styles.infoSubtitle}>
              seamlessly connected.
            </Text>

          </View>

          {/* Stats */}

          <View style={styles.statsContainer}>

            <View style={styles.statCard}>
              <Text style={styles.statNumber}>Medical</Text>
              <Text style={styles.statLabel}>Records</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statNumber}>Analysis</Text>
              <Text style={styles.statLabel}>And alerts</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statNumber}>24×7</Text>
              <Text style={styles.statLabel}>Access</Text>
            </View>

          </View>

          {/* Loading */}

          <View style={styles.loadingContainer}>

            <View style={styles.loadingHeader}>

              <Text style={styles.loadingText}>
                INITIALIZING...
              </Text>

              <Text style={styles.loadingPercent}>
                {progress}%
              </Text>

            </View>

            <View style={styles.progressBackground}>

              <View
                style={[
                  styles.progressFill,
                  {
                    width: `${progress}%`,
                  },
                ]}
              />

            </View>

          </View>

        </SafeAreaView>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({

  gradient: {
    flex: 1,
  },

  phone: {
    flex: 1,
    width: "100%",
    alignItems: "center",
  },

  container: {
    flex: 1,
    width: "100%",
    maxWidth: 430,
    justifyContent: "space-evenly",
    alignItems: "center",
    paddingHorizontal: 24,
    overflow: "hidden",
  },

  circle1: {
    position: "absolute",
    width: 250,
    height: 250,
    borderRadius: 125,
    backgroundColor: "#D9ECFA",
    top: -80,
    right: -100,
    opacity: 0.35,
  },

  circle2: {
    position: "absolute",
    width: 180,
    height: 180,
    borderRadius: 90,
    backgroundColor: "#EAF6FD",
    bottom: 80,
    left: -70,
    opacity: 0.55,
  },

  circle3: {
    position: "absolute",
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: "#CFE8F8",
    bottom: 220,
    right: -30,
    opacity: 0.35,
  },

  versionContainer: {
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 25,
    borderWidth: 1,
    borderColor: "#D7EAF6",
    backgroundColor: "rgba(255,255,255,0.75)",
  },

  version: {
    fontSize: 11,
    letterSpacing: 2,
    fontWeight: "700",
    color: "#7391A8",
  },

  title: {
    fontSize: 52,
    fontWeight: "900",
    color: "#244C69",
    marginTop: -10,
  },

  subtitleRow: {
    flexDirection: "row",
    alignItems: "center",
  },

  line: {
    width: 40,
    height: 1,
    backgroundColor: "#BFD8EA",
    marginHorizontal: 10,
  },

  subtitle: {
    fontSize: 11,
    letterSpacing: 3,
    color: "#6F90A8",
    fontWeight: "700",
  },

  infoCard: {
    width: "100%",
    backgroundColor: "rgba(255,255,255,0.80)",
    borderRadius: 24,
    paddingVertical: 24,
    borderWidth: 1,
    borderColor: "#E3EEF7",

    shadowColor: "#80A7C8",
    shadowOpacity: 0.10,
    shadowRadius: 20,
    shadowOffset: {
      width: 0,
      height: 10,
    },

    elevation: 5,
  },

  infoTitle: {
    textAlign: "center",
    fontSize: 22,
    fontWeight: "700",
    color: "#365D79",
  },

  infoSubtitle: {
    textAlign: "center",
    fontSize: 18,
    color: "#6E8DA6",
    marginTop: 5,
  },

  statsContainer: {
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-between",
  },

  statCard: {
    width: "31%",
    paddingVertical: 20,
    borderRadius: 20,
    alignItems: "center",

    backgroundColor: "rgba(255,255,255,0.85)",

    borderWidth: 1,
    borderColor: "#E2EDF7",

    shadowColor: "#7EA8CC",
    shadowOpacity: 0.08,
    shadowRadius: 10,
    shadowOffset: {
      width: 0,
      height: 5,
    },

    elevation: 4,
  },

  statNumber: {
    fontSize: 22,
    fontWeight: "800",
    color: "#2B4F6B",
  },

  statLabel: {
    marginTop: 5,
    fontSize: 12,
    color: "#7C97AD",
  },

  loadingContainer: {
    width: "100%",
  },

  loadingHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 12,
  },

  loadingText: {
    color: "#3B607B",
    fontWeight: "700",
    letterSpacing: 1,
  },

  loadingPercent: {
    color: "#4E89B9",
    fontWeight: "800",
  },

  progressBackground: {
    width: "100%",
    height: 12,
    borderRadius: 12,
    backgroundColor: "#D8EAF6",
    overflow: "hidden",
  },

  progressFill: {
    height: "100%",
    borderRadius: 12,
    backgroundColor: "#4E89B9",
  },

});