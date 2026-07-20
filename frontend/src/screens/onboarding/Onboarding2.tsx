import React from "react";
import {
  SafeAreaView,
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  useWindowDimensions,
  Platform,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import AnimatedLogo from "../../components/AnimatedLogo";
import SkipButton from "../../components/SkipButton";
import OnboardingHeader from "../../components/OnboardingHeader";
import TimelineSection from "../../components/TimelineSection";
import FloatingGlow from "../../components/FloatingGlow";

export default function Onboarding2() {

  const navigation = useNavigation<any>();

  const { width } = useWindowDimensions();

  const isDesktop = width > 1100;
  const isTablet = width > 768;

  return (

    <LinearGradient
      colors={[
        "#FCFEFF",
        "#F4FAFD",
        "#EEF8FD",
        "#FCFEFF",
      ]}
      style={styles.container}
    >

      {/* Floating Background */}

      <View style={styles.circle1}/>
      <View style={styles.circle2}/>
      <View style={styles.circle3}/>
      <View style={styles.circle4}/>

      <SafeAreaView style={styles.safeArea}>

        <ScrollView
          contentContainerStyle={[
            styles.scroll,

            {
              alignItems: "center"
            }

          ]}
          showsVerticalScrollIndicator={false}
        >

          <View

            style={[

              styles.content,

              {

                width:"100%",

                maxWidth:isDesktop
                  ?1000
                  :isTablet
                  ?700
                  :430

              }

            ]}

          >

            {/* Header */}

            <View style={styles.topBar}>

              <View style={styles.logoArea}>

                <AnimatedLogo/>

                <View style={{marginLeft:16}}>

                  <Text style={styles.logoText}>
                    Medilink
                  </Text>

                  <Text style={styles.logoSub}>
                    HEALTH PLATFORM
                  </Text>

                </View>

              </View>

              <SkipButton/>

            </View>

            {/* Heading */}

            <OnboardingHeader/>

            {/* Floating Glow */}

            <FloatingGlow/>

            {/* Timeline Card */}

            <View style={styles.timelineCard}>

              <View style={styles.timelineHeader}>

                <View>

                  <Text style={styles.timelineTitle}>
                    Patient Timeline
                  </Text>

                  <Text style={styles.timelineSubtitle}>
                    Unified medical history
                  </Text>

                </View>

                <View style={styles.syncBadge}>

                  <Ionicons
                    name="cloud-done"
                    size={18}
                    color="#4E89B9"
                  />

                  <Text style={styles.syncText}>
                    Synced
                  </Text>

                </View>

              </View>

              <TimelineSection/>

            </View>

            {/* Bottom */}

            <View style={styles.bottomContainer}>

              {/* Indicators */}

              <View style={styles.indicators}>

                <View style={styles.dot}/>

                <View style={styles.activeDot}/>

                <View style={styles.dot}/>

              </View>

              {/* Continue */}

              <TouchableOpacity

                activeOpacity={0.9}

                style={styles.continueButton}

                onPress={() =>
                  navigation.navigate("Onboarding3")
                }

              >

                <Text style={styles.continueText}>
                  Continue
                </Text>

                <Ionicons

                  name="arrow-forward"

                  color="#fff"

                  size={22}

                />

              </TouchableOpacity>

            </View>

          </View>

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
  },

  scroll: {
    flexGrow: 1,
    justifyContent: "center",
    paddingVertical: 35,
    paddingHorizontal: 20,
  },

  content: {
    alignSelf: "center",
  },

  /* ---------------- Background ---------------- */

  circle1: {
    position: "absolute",
    width: 420,
    height: 420,
    borderRadius: 210,
    backgroundColor: "#D9EEFB",
    top: -150,
    right: -150,
    opacity: 0.55,
  },

  circle2: {
    position: "absolute",
    width: 260,
    height: 260,
    borderRadius: 130,
    backgroundColor: "#EDF8FF",
    bottom: -50,
    left: -90,
    opacity: 0.85,
  },

  circle3: {
    position: "absolute",
    width: 170,
    height: 170,
    borderRadius: 85,
    backgroundColor: "#D7ECFA",
    top: 260,
    left: -60,
    opacity: 0.45,
  },

  circle4: {
    position: "absolute",
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: "#DCEFFC",
    bottom: 260,
    right: -30,
    opacity: 0.6,
  },

  /* ---------------- Header ---------------- */

  topBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 35,
  },

  logoArea: {
    flexDirection: "row",
    alignItems: "center",
  },

  logoText: {
    fontSize: 28,
    fontWeight: "800",
    color: "#234964",
    letterSpacing: 0.4,
  },

  logoSub: {
    marginTop: 2,
    fontSize: 11,
    color: "#86A4B9",
    letterSpacing: 2.2,
    fontWeight: "600",
  },

  /* ---------------- Timeline Card ---------------- */

  timelineCard: {
    marginTop: 35,

    backgroundColor: "rgba(255,255,255,0.88)",

    borderRadius: 34,

    padding: 26,

    borderWidth: 1,

    borderColor: "#E5F2FA",

    shadowColor: "#5E95C6",

    shadowOpacity: 0.16,

    shadowRadius: 28,

    shadowOffset: {
      width: 0,
      height: 14,
    },

    elevation: 12,
  },

  timelineHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 22,
  },

  timelineTitle: {
    fontSize: 24,
    fontWeight: "800",
    color: "#214A68",
  },

  timelineSubtitle: {
    marginTop: 4,
    fontSize: 15,
    color: "#89A2B7",
  },

  syncBadge: {
    flexDirection: "row",
    alignItems: "center",

    paddingHorizontal: 15,
    paddingVertical: 10,

    borderRadius: 24,

    backgroundColor: "#EEF8FF",

    borderWidth: 1,
    borderColor: "#D8ECFA",
  },

  syncText: {
    marginLeft: 6,
    fontSize: 13,
    color: "#4E89B9",
    fontWeight: "700",
  },

  /* ---------------- Bottom ---------------- */

  bottomContainer: {
    marginTop: 40,
    alignItems: "center",
  },

  indicators: {
    flexDirection: "row",
    marginBottom: 26,
  },

  dot: {
    width: 11,
    height: 11,
    borderRadius: 6,
    backgroundColor: "#D8E9F7",
    marginHorizontal: 6,
  },

  activeDot: {
    width: 34,
    height: 11,
    borderRadius: 6,
    backgroundColor: "#4E89B9",
    marginHorizontal: 6,
  },

  continueButton: {
    width: "100%",
    height: 62,

    borderRadius: 32,

    backgroundColor: "#4E89B9",

    justifyContent: "center",
    alignItems: "center",

    flexDirection: "row",

    shadowColor: "#4E89B9",

    shadowOpacity: 0.35,

    shadowRadius: 18,

    shadowOffset: {
      width: 0,
      height: 10,
    },

    elevation: 12,
  },

  continueText: {
    color: "#FFFFFF",
    fontSize: 19,
    fontWeight: "700",
    marginRight: 10,
  },

});