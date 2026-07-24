import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import { useStyles } from "../../hooks/useStyles";
import { Ionicons } from "@expo/vector-icons";
import {
  getNotifications,
} from "../../services/notificationService";

import { useEffect, useState } from "react";
export default function Dashboard() {
  const navigation = useNavigation<any>();
  const { colors, globalStyles } = useStyles();
  const [unreadCount, setUnreadCount] = useState(0);
  useEffect(() => {
  loadUnreadCount();
}, []);

const loadUnreadCount = async () => {
  try {
    const notifications = await getNotifications();

    const unread = notifications.filter(
      (item: any) => !item.is_read
    );

    setUnreadCount(unread.length);
  } catch (err) {
    console.log(err);
  }
};
  return (
    <View
      style={[
        globalStyles.screen,
        styles.container,
      ]}
    >
      <View style={styles.header}>
  <Text
    style={[
      styles.title,
      { color: colors.primary },
    ]}
  >
    Medilink Dashboard
  </Text>

  <TouchableOpacity
    onPress={() =>
      navigation.navigate("Notifications")
    }
  >
    <View>
      <Ionicons
        name="notifications"
        size={30}
        color={colors.primary}
      />

      {/* Badge */}
      {unreadCount > 0 && (
  <View style={styles.badge}>
    <Text style={styles.badgeText}>
      {unreadCount}
    </Text>
  </View>
)}
    </View>
  </TouchableOpacity>
</View>

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

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate("Trend")}
>
        <Text style={styles.buttonText}>
          Trend Analysis
        </Text>
      </TouchableOpacity>
      <TouchableOpacity
  style={styles.button}
  onPress={() => navigation.navigate("Anomaly")}
>
  <Text style={styles.buttonText}>
    Personal Baseline & Anomalies
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
  header: {
  width: "100%",
  flexDirection: "row",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: 40,
},

badge: {
  position: "absolute",
  top: -5,
  right: -6,

  width: 18,
  height: 18,

  borderRadius: 9,

  backgroundColor: "#EF4444",

  justifyContent: "center",
  alignItems: "center",
},

badgeText: {
  color: "#FFFFFF",
  fontSize: 10,
  fontWeight: "700",
},
});