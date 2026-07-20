import React, { useEffect, useState } from "react";
import { getProfile, Profile } from "../../services/profileService";
import {
  SafeAreaView,
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { useNavigation } from "@react-navigation/native";
import { Ionicons } from "@expo/vector-icons";

import ProfileAvatar from "../../components/profile/ProfileAvatar";
import InfoCard from "../../components/profile/InfoCard";
import PrimaryButton from "../../components/profile/PrimaryButton";
import { useFocusEffect } from "@react-navigation/native";
import { removeToken } from "../../utils/storage";
import { Alert, Platform } from "react-native";
import { useCallback } from "react";
const { width } = Dimensions.get("window");
import { useTheme } from "../../theme/ThemeContext";
export default function ProfileScreen() {

  const navigation = useNavigation<any>();
  const { colors, darkMode } = useTheme();
  const [profile, setProfile] = useState<Profile | null>(null);

  const [loading, setLoading] = useState(true);
  useFocusEffect(
  useCallback(() => {
    loadProfile();
  }, [])
);

const loadProfile = async () => {
  try {
    const data = await getProfile();

    console.log("PROFILE DATA =", data);

    setProfile(data);
  } catch (error) {
    console.log("Profile Error:", error);
  } finally {
    setLoading(false);
  }
};
if (loading) {

  return (

    <SafeAreaView
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >

      <Text>Loading...</Text>

    </SafeAreaView>

  );

}
const handleLogout = async () => {
  if (Platform.OS === "web") {
    const confirmed = window.confirm(
      "Are you sure you want to logout?"
    );

    if (!confirmed) return;

    await removeToken();

    navigation.reset({
      index: 0,
      routes: [{ name: "Login" }],
    });

    return;
  }

  Alert.alert(
    "Logout",
    "Are you sure you want to logout?",
    [
      {
        text: "Cancel",
        style: "cancel",
      },
      {
        text: "Logout",
        style: "destructive",
        onPress: async () => {
          await removeToken();

          navigation.reset({
            index: 0,
            routes: [{ name: "Login" }],
          });
        },
      },
    ]
  );
};
  return (

    <SafeAreaView
  style={[
    styles.container,
    {
      backgroundColor: colors.background,
    },
  ]}
>

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scroll}
      >

        {/* Header */}

        <LinearGradient
  colors={
    darkMode
      ? ["#1E293B", "#111827", "#000000"]
      : ["#4E89B9", "#2563EB"]
  }
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.headerGradient}
        >

          {/* Top Row */}

          <View style={styles.header}>

            <TouchableOpacity onPress={() => {
    if (navigation.canGoBack()) {
      navigation.goBack();
    } else {
      navigation.navigate("Dashboard");
    }
  }}>

              <Ionicons
                name="arrow-back"
                size={24}
                color="#FFFFFF"
              />

            </TouchableOpacity>

            <Text style={styles.headerTitle}>
              My Profile
            </Text>

            <TouchableOpacity
  onPress={() => navigation.navigate("Settings")}
>

  <Ionicons
    name="settings-outline"
    size={24}
    color="#FFFFFF"
  />

</TouchableOpacity>

          </View>

          {/* Avatar */}

          <ProfileAvatar
  name={profile?.name ?? ""}
  role="Medical Records Owner"
  image={
    profile?.profile_image
      ? { uri: profile.profile_image }
      : undefined
  }
  onEdit={() => navigation.navigate("EditProfile")}
/>

          {/* Premium Badge */}

          <View
  style={[
    styles.badge,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
>

            <Ionicons
              name="shield-checkmark"
              size={18}
              color="#2563EB"
            />

            <Text
  style={[
    styles.badgeText,
    {
      color: colors.primary,
    },
  ]}
>
              Verified Health Profile
            </Text>

          </View>

        </LinearGradient>

        {/* Quick Stats */}

        <View style={styles.statsRow}>

          <View
  style={[
    styles.statCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
>

            <Ionicons
              name="document-text"
              size={26}
              color="#2563EB"
            />

            <Text style={styles.statNumber}>
              24
            </Text>

            <Text style={styles.statLabel}>
              Reports
            </Text>

          </View>

          <View
  style={[
    styles.statCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
>

            <Ionicons
              name="analytics"
              size={26}
              color="#2563EB"
            />

            <Text style={styles.statNumber}>
              18
            </Text>

            <Text style={styles.statLabel}>
              Trends
            </Text>

          </View>

          <View
  style={[
    styles.statCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
>

            <Ionicons
              name="chatbubbles"
              size={26}
              color="#2563EB"
            />

            <Text style={styles.statNumber}>
              12
            </Text>

            <Text style={styles.statLabel}>
              AI Chats
            </Text>

          </View>

        </View>

        {/* Personal Information */}

        <Text
  style={[
    styles.sectionTitle,
    {
      color: colors.text,
    },
  ]}
>
          Personal Information
        </Text>
        {/* Personal Information */}

<InfoCard
  icon="mail-outline"
  title="Email"
  value={profile?.email ?? ""}
/>

<InfoCard
  icon="call-outline"
  title="Phone Number"
  value={profile?.phone ?? ""}
/>

<InfoCard
  icon="water-outline"
  title="Blood Group"
  value={profile?.blood_group ?? ""}
/>

<InfoCard
  icon="female-outline"
  title="Gender"
  value={profile?.gender ?? ""}
/>

<InfoCard
  icon="calendar-outline"
  title="Age"
  value={profile?.dob ?? ""}
/>

{/* ---------------- Health Overview ---------------- */}

<View
  style={[
    styles.healthCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
>

  <View style={styles.healthHeader}>

    <Text
  style={[
    styles.healthTitle,
    {
      color: colors.text,
    },
  ]}
>
      Health Overview
    </Text>

    <Ionicons
      name="heart"
      size={24}
      color="#EF4444"
    />

  </View>

  <Text
  style={[
    styles.healthDescription,
    {
      color: colors.subText,
    },
  ]}
>
    Your recent health reports indicate stable vitals.
    Continue maintaining a healthy lifestyle and regular
    checkups.
  </Text>

</View>

{/* ---------------- Quick Actions ---------------- */}

<Text
  style={[
    styles.sectionTitle,
    {
      color: colors.text,
    },
  ]}
>
  Quick Actions
</Text>

<View style={styles.quickGrid}>

  <TouchableOpacity
    style={[
    styles.quickCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
    onPress={() => navigation.navigate("Settings")}
  >

    <View
  style={[
    styles.quickIcon,
    {
      backgroundColor: darkMode ? "#2A2A2A" : "#EEF6FF",
    },
  ]}
>

      <Ionicons
        name="settings-outline"
        size={28}
        color="#2563EB"
      />

    </View>

    <Text
  style={[
    styles.quickTitle,
    {
      color: colors.text,
    },
  ]}
>
      Settings
    </Text>

  </TouchableOpacity>

  <TouchableOpacity
    style={[
    styles.quickCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
    onPress={() => navigation.navigate("Privacy")}
  >

    <View
  style={[
    styles.quickIcon,
    {
      backgroundColor: darkMode ? "#2A2A2A" : "#EEF6FF",
    },
  ]}
>

      <Ionicons
        name="shield-checkmark-outline"
        size={28}
        color="#2563EB"
      />

    </View>

    <Text
  style={[
    styles.quickTitle,
    {
      color: colors.text,
    },
  ]}
>
      Privacy
    </Text>

  </TouchableOpacity>

  <TouchableOpacity
    style={[
    styles.quickCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.shadow,
    },
  ]}
    onPress={() => navigation.navigate("HelpSupport")}
  >

    <View
  style={[
    styles.quickIcon,
    {
      backgroundColor: darkMode ? "#2A2A2A" : "#EEF6FF",
    },
  ]}
>

      <Ionicons
        name="help-circle-outline"
        size={28}
        color="#2563EB"
      />

    </View>

    <Text
  style={[
    styles.quickTitle,
    {
      color: colors.text,
    },
  ]}
>
      Help
    </Text>

  </TouchableOpacity>

</View>

{/* ---------------- Buttons ---------------- */}

<View style={{ marginTop: 28 }}>

  <PrimaryButton
    title="Edit Profile"
    icon="create-outline"
    onPress={() => navigation.navigate("EditProfile")}
  />

</View>

<TouchableOpacity
  style={[
    styles.logoutButton,
    {
      backgroundColor: darkMode ? "#2B1D1D" : "#FFF5F5",
      borderColor: colors.danger,
    },
  ]}
  onPress={handleLogout}
>

  <Ionicons
    name="log-out-outline"
    size={22}
    color="#EF4444"
  />

  <Text
  style={[
    styles.logoutText,
    {
      color: colors.danger,
    },
  ]}
>
    Logout
  </Text>

</TouchableOpacity>

</ScrollView>

</SafeAreaView>

);

}
const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: "#F5F9FC",
  },

  scroll: {
    paddingBottom: 40,
  },

  /* ---------------- HEADER ---------------- */

  headerGradient: {
    paddingTop: 20,
    paddingHorizontal: width > 900 ? 60 : 22,
    paddingBottom: 35,
    borderBottomLeftRadius: 35,
    borderBottomRightRadius: 35,
  },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 18,
  },

  headerTitle: {
    color: "#FFFFFF",
    fontSize: 24,
    fontWeight: "700",
  },

  /* ---------------- BADGE ---------------- */

  badge: {
    alignSelf: "center",
    marginTop: 15,

    flexDirection: "row",
    alignItems: "center",

    backgroundColor: "#FFFFFF",

    paddingHorizontal: 18,
    paddingVertical: 10,

    borderRadius: 22,

    shadowColor: "#000",
    shadowOpacity: .08,
    shadowRadius: 8,
    elevation: 5,
  },

  badgeText: {
    marginLeft: 8,
    color: "#2563EB",
    fontWeight: "700",
    fontSize: 14,
  },

  /* ---------------- QUICK STATS ---------------- */

  statsRow: {

    flexDirection: "row",

    justifyContent: "space-between",

    marginHorizontal: width > 900 ? 60 : 20,

    marginTop: -25,

  },

  statCard: {

    width: "31%",

    backgroundColor: "#FFFFFF",

    borderRadius: 22,

    paddingVertical: 22,

    alignItems: "center",

    shadowColor: "#000",

    shadowOpacity: .08,

    shadowRadius: 10,

    shadowOffset: {
      width: 0,
      height: 5,
    },

    elevation: 5,

  },

  statNumber: {

    marginTop: 10,

    fontSize: 24,

    fontWeight: "800",

    color: "#2563EB",

  },

  statLabel: {

    marginTop: 5,

    color: "#64748B",

    fontSize: 13,

  },

  /* ---------------- SECTION ---------------- */

  sectionTitle: {

    marginTop: 30,

    marginBottom: 16,

    marginHorizontal: width > 900 ? 60 : 20,

    fontSize: 22,

    fontWeight: "700",

    color: "#1E293B",

  },

  /* ---------------- HEALTH CARD ---------------- */

  healthCard: {

    marginHorizontal: width > 900 ? 60 : 20,

    marginTop: 15,

    backgroundColor: "#FFFFFF",

    borderRadius: 22,

    padding: 22,

    shadowColor: "#000",

    shadowOpacity: .06,

    shadowRadius: 12,

    elevation: 5,

  },

  healthHeader: {

    flexDirection: "row",

    justifyContent: "space-between",

    alignItems: "center",

    marginBottom: 14,

  },

  healthTitle: {

    fontSize: 20,

    fontWeight: "700",

    color: "#1E293B",

  },

  healthDescription: {

    color: "#64748B",

    lineHeight: 26,

    fontSize: 15,

  },

  /* ---------------- QUICK ACTIONS ---------------- */

  quickGrid: {

    flexDirection: width > 900 ? "row" : "column",

    justifyContent: "space-between",

    marginHorizontal: width > 900 ? 60 : 20,

  },

  quickCard: {

    flex: width > 900 ? 1 : undefined,

    backgroundColor: "#FFFFFF",

    marginBottom: 18,

    marginHorizontal: width > 900 ? 8 : 0,

    borderRadius: 22,

    paddingVertical: 28,

    alignItems: "center",

    shadowColor: "#000",

    shadowOpacity: .06,

    shadowRadius: 10,

    elevation: 5,

  },

  quickIcon: {

    width: 62,

    height: 62,

    borderRadius: 18,

    backgroundColor: "#EEF6FF",

    justifyContent: "center",

    alignItems: "center",

    marginBottom: 14,

  },

  quickTitle: {

    fontSize: 17,

    fontWeight: "700",

    color: "#334155",

  },

  /* ---------------- BUTTON ---------------- */

  logoutButton: {

    marginHorizontal: width > 900 ? 60 : 20,

    marginTop: 18,

    marginBottom: 35,

    height: 56,

    borderRadius: 18,

    borderWidth: 1,

    borderColor: "#FECACA",

    backgroundColor: "#FFF5F5",

    flexDirection: "row",

    justifyContent: "center",

    alignItems: "center",

  },

  logoutText: {

    marginLeft: 10,

    color: "#DC2626",

    fontWeight: "700",

    fontSize: 17,

  },

});