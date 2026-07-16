import React, { useEffect, useRef } from "react";
import {
  SafeAreaView,
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Animated,
  Dimensions,
  ScrollView,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import AnimatedLogo from "../../components/AnimatedLogo";
import SkipButton from "../../components/SkipButton";
import AIOrb from "../../components/AIOrb";
import ChatBubble from "../../components/ChatBubble";
import PoweredBadge from "../../components/PoweredBadge";

const { width } = Dimensions.get("window");

export default function Onboarding3() {
  const navigation = useNavigation<any>();

  const fade = useRef(new Animated.Value(0)).current;
  const slide = useRef(new Animated.Value(35)).current;

  const bubble1 = useRef(new Animated.Value(0)).current;
  const bubble2 = useRef(new Animated.Value(0)).current;
  const bubble3 = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fade, {
        toValue: 1,
        duration: 900,
        useNativeDriver: true,
      }),
      Animated.timing(slide, {
        toValue: 0,
        duration: 900,
        useNativeDriver: true,
      }),
    ]).start();

    Animated.loop(
      Animated.sequence([
        Animated.parallel([
          Animated.timing(bubble1, {
            toValue: -10,
            duration: 1800,
            useNativeDriver: true,
          }),
          Animated.timing(bubble2, {
            toValue: 10,
            duration: 1800,
            useNativeDriver: true,
          }),
          Animated.timing(bubble3, {
            toValue: -8,
            duration: 1800,
            useNativeDriver: true,
          }),
        ]),
        Animated.parallel([
          Animated.timing(bubble1, {
            toValue: 0,
            duration: 1800,
            useNativeDriver: true,
          }),
          Animated.timing(bubble2, {
            toValue: 0,
            duration: 1800,
            useNativeDriver: true,
          }),
          Animated.timing(bubble3, {
            toValue: 0,
            duration: 1800,
            useNativeDriver: true,
          }),
        ]),
      ])
    ).start();
  }, []);

  return (
    <LinearGradient colors={["#FCFEFF", "#EEF6FD", "#FCFEFF"]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.logoRow}>
            <AnimatedLogo />
            <Text style={styles.logo}>Medilink</Text>
          </View>

          <SkipButton />
        </View>

        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          <Animated.View
            style={{
              opacity: fade,
              transform: [{ translateY: slide }],
            }}
          >
          {/* AI Illustration */}
          <View style={styles.illustrationContainer}>
            {/* Left Bubble */}
            <Animated.View
              style={[
                styles.leftBubble,
                { transform: [{ translateY: bubble1 }] },
              ]}
            >
              <ChatBubble sender="You" message="Can you summarize my blood report?" />
            </Animated.View>
            

            {/* AI Orb */}
            <View style={styles.orbContainer}>
              <AIOrb />
            </View>

            {/* Right Bubble */}
            <Animated.View
              style={[
                styles.rightBubble,
                { transform: [{ translateY: bubble2 }] },
              ]}
            >
              <ChatBubble
                ai
                sender="AI Assistant"
                message="Your overall health looks stable. Vitamin D is slightly low."
              />
            </Animated.View>

            {/* Bottom Bubble */}
            <Animated.View
              style={[
                styles.bottomBubble,
                { transform: [{ translateY: bubble3 }] },
              ]}
            >
              <ChatBubble sender="Follow Up" message="Would you like lifestyle recommendations?" />
            </Animated.View>
          </View>

          {/* Powered Badge */}
          <PoweredBadge />

          {/* Heading */}
          <Text style={styles.title}>AI Powered{"\n"}Health Assistant</Text>

          {/* Subtitle */}
          <Text style={styles.subtitle}>
            Ask questions about your reports, understand
            trends, receive personalized insights, and chat
            securely with Medilink AI.
          </Text>

          {/* Page Indicators */}
          <View style={styles.indicatorContainer}>
            <View style={styles.dot} />
            <View style={styles.dot} />
            <View style={styles.activeDot} />
          </View>

          {/* Get Started Button */}
          <TouchableOpacity
            activeOpacity={0.9}
            style={styles.startButton}
            onPress={() => navigation.replace("Login")}
          >
            <LinearGradient
              colors={["#5D9DFF", "#4E89B9"]}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.gradientButton}
            >
              <Text style={styles.startText}>Get Started</Text>
              <Ionicons name="arrow-forward" size={20} color="#FFFFFF" />
            </LinearGradient>
          </TouchableOpacity>

          {/* Login */}
          <TouchableOpacity onPress={() => navigation.replace("Login")}>
            <Text style={styles.loginText}>
              Already have an account?
              <Text style={styles.loginNow}> Login</Text>
            </Text>
          </TouchableOpacity>
        </Animated.View>
        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  safeArea: {
    flex: 1,
    paddingHorizontal: width > 900 ? 80 : 24,
    paddingTop: 20,
  },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 25,
  },

  logoRow: {
    flexDirection: "row",
    alignItems: "center",
  },

  logo: {
    fontSize: 22,
    fontWeight: "800",
    marginLeft: 12,
    color: "#264B68",
  },

  scrollContent: {
    flexGrow: 1,
    paddingBottom: 40,
  },

  illustrationContainer: {
    alignItems: "center",
    justifyContent: "center",
    height: width > 900 ? 420 : 360,
    marginBottom: 20,
  },

  orbContainer: {
    justifyContent: "center",
    alignItems: "center",
  },

  leftBubble: {
    position: "absolute",
    left: width > 900 ? width * 0.18 : 0,
    top: width > 900 ? 20 : 40,
  },

  rightBubble: {
    position: "absolute",
    right: width > 900 ? width * 0.18 : 0,
    top: width > 900 ? 50 : 65,
  },

  bottomBubble: {
    position: "absolute",
    bottom: width > 900 ? 20 : 10,
    alignSelf: "center",
  },

  title: {
    marginTop: 20,
    textAlign: "center",
    fontSize: width > 900 ? 44 : 34,
    fontWeight: "800",
    color: "#244C69",
    lineHeight: width > 900 ? 56 : 44,
  },

  subtitle: {
    marginTop: 18,
    textAlign: "center",
    color: "#6F8CA4",
    fontSize: 16,
    lineHeight: 28,
    paddingHorizontal: width > 900 ? 180 : 12,
  },

  indicatorContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 30,
    marginBottom: 35,
  },

  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#D6E6F4",
    marginHorizontal: 6,
  },

  activeDot: {
    width: 30,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#4E89B9",
    marginHorizontal: 6,
  },

  startButton: {
    alignSelf: "center",
    width: width > 900 ? 320 : "100%",
    borderRadius: 32,

    shadowColor: "#4E89B9",
    shadowOpacity: 0.35,
    shadowRadius: 16,
    shadowOffset: {
      width: 0,
      height: 8,
    },

    elevation: 8,
  },

  gradientButton: {
    height: 60,
    borderRadius: 32,

    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },

  startText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
    marginRight: 10,
  },

  loginText: {
    marginTop: 24,
    marginBottom: 20,
    textAlign: "center",
    color: "#7B94AA",
    fontSize: 15,
  },

  loginNow: {
    color: "#4E89B9",
    fontWeight: "700",
  },
});