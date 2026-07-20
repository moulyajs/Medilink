
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import { useEffect } from "react";
import { getProfile, Profile } from "../../services/profileService";
import SettingsItem from "../../components/settings/SettingsItem";
import React, { useState } from "react";
import { useTheme } from "../../theme/ThemeContext";
export default function SettingsScreen() {

  const navigation = useNavigation<any>();
  const [profile, setProfile] = useState<Profile | null>(null);

useEffect(() => {
  loadProfile();
}, []);

const loadProfile = async () => {
  try {
    const data = await getProfile();
    setProfile(data);
  } catch (err) {
    console.log(err);
  }
};

  const [notifications, setNotifications] =
    useState(true);

  const { darkMode, setDarkMode, colors } = useTheme();
  return (

   
    <SafeAreaView
  style={[
    styles.container,
    { backgroundColor: colors.background },
  ]}>
      <ScrollView
  showsVerticalScrollIndicator={false}
  contentContainerStyle={{ paddingBottom: 30 }}
>

        {/* Header */}

        <LinearGradient
           colors={
    darkMode
      ? ["#1E293B", "#111827", "#000000"]
      : ["#5D9DFF", "#4E89B9", "#2563EB"]
  }
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.header}
        >

          <View style={styles.headerRow}>

            <Ionicons
              name="settings"
              size={34}
              color="#FFFFFF"
            />

            <Text style={styles.headerTitle}>
              Settings
            </Text>

          </View>

          <Text style={styles.headerSubtitle}>
            Customize your Medilink experience
          </Text>

        </LinearGradient>

        {/* Profile Card */}

        <View
  style={[
    styles.profileCard,
    {
      backgroundColor: colors.card,
      shadowColor: colors.text,
    },
  ]}
>
<View
  style={[
    styles.avatar,
    {
      backgroundColor: colors.primary,
    },
  ]}
>

            <Ionicons
              name="person"
              size={42}
              color="#FFFFFF"
            />

          </View>

          <View style={{ flex: 1 }}>

           <Text
  style={[
    styles.name,
    { color: colors.text },
  ]}>
  {profile?.name}
</Text>

<Text
  style={[
    styles.email,
    { color: colors.text },
  ]}>
  {profile?.email}
</Text>

          </View>

        </View>
                {/* Preferences */}

        <Text
  style={[
    styles.sectionTitle,
    { color: colors.text },
  ]}>
          Preferences
        </Text>

       <SettingsItem
  icon="notifications-outline"
  title="Notifications"
  subtitle="Manage notification preferences"
  onPress={() =>
    navigation.navigate("NotificationSettings")
  }
/>

        <SettingsItem
          icon="moon-outline"
          title="Dark Mode"
          subtitle="Switch between light and dark theme"
          showSwitch
          switchValue={darkMode}
          onSwitchChange={setDarkMode}
        />

        {/* Security */}

        <Text
  style={[
    styles.sectionTitle,
    { color: colors.text },
  ]}>
          Security
        </Text>

        <SettingsItem
          icon="shield-checkmark-outline"
          title="Privacy & Security"
          subtitle="Biometric, PIN and sessions"
          onPress={() =>
            navigation.navigate("Privacy")
          }
        />

        {/* Support */}

        <Text
  style={[
    styles.sectionTitle,
    { color: colors.text },
  ]}>
          Support
        </Text>

        <SettingsItem
          icon="help-circle-outline"
          title="Help & Support"
          subtitle="FAQ, Contact us, Report Issue"
          onPress={() =>
            navigation.navigate("HelpSupport")
          }
        />

        <SettingsItem
  icon="information-circle-outline"
  title="About Medilink"
  subtitle="Version 1.0.0"
  onPress={() =>
    navigation.navigate("AboutMedilink")
  }
/>

        {/* Logout */}

        <Text
  style={[
    styles.sectionTitle,
    { color: colors.text },
  ]}>
          Account
        </Text>

        <SettingsItem
          icon="log-out-outline"
          title="Logout"
          subtitle="Sign out from your account"
          danger
          onPress={() => {
             
          }}
        />
              </ScrollView>

    </SafeAreaView>
  );
}
const styles = StyleSheet.create({

  container: {
    flex: 1,
  },

  /* ---------------- Header ---------------- */

  header: {
    paddingTop: 28,
    paddingBottom: 45,
    paddingHorizontal: 24,

    borderBottomLeftRadius: 35,
    borderBottomRightRadius: 35,
  },

  headerRow: {
    flexDirection: "row",
    alignItems: "center",
  },

  headerTitle: {
    marginLeft: 12,
    color: "#FFFFFF",
    fontSize: 28,
    fontWeight: "700",
  },

  headerSubtitle: {
    color: "#EAF4FF",
    marginTop: 14,
    fontSize: 15,
    lineHeight: 22,
  },

  /* ---------------- Profile Card ---------------- */

  profileCard: {
    flexDirection: "row",
  alignItems: "center",

  marginHorizontal: 20,
  marginTop: -25,

  padding: 18,

  borderRadius: 22,

  shadowOpacity: 0.08,
  shadowRadius: 14,
  shadowOffset: {
    width: 0,
    height: 6,
  },

  elevation: 6,
  },

  avatar: {
    width: 65,
    height: 65,

    borderRadius: 32.5,

    justifyContent: "center",
    alignItems: "center",

    marginRight: 18,
  },

  name: {
    fontSize: 20,
    fontWeight: "700",
  },

  email: {
    marginTop: 4,
    fontSize: 14,
  },

  /* ---------------- Section ---------------- */

  sectionTitle: {
    marginTop: 28,
    marginBottom: 12,
    marginLeft: 24,

    fontSize: 18,
    fontWeight: "700",
  },

});