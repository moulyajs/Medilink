import React, { useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import { getProfile } from "../../services/profileService";
import { sendSupportMessage } from "../../services/supportService";
import { useTheme } from "../../theme/ThemeContext";

export default function ContactSupportScreen() {
  const navigation = useNavigation<any>();
  const { colors, darkMode } = useTheme();

  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!subject.trim() || !message.trim()) {
      Alert.alert(
        "Missing Information",
        "Please complete all fields."
      );
      return;
    }

    try {
      setLoading(true);

      const profile = await getProfile();

      await sendSupportMessage({
        email: profile.email,
        subject,
        message,
      });

      Alert.alert(
        "Success",
        "Your support request has been sent successfully."
      );

      setSubject("");
      setMessage("");
    } catch (error) {
      console.log(error);

      Alert.alert(
        "Error",
        "Failed to send support request."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView
      style={[
        styles.container,
        { backgroundColor: colors.background },
      ]}
    >
      <LinearGradient
        colors={
          darkMode
            ? ["#1E293B", "#111827", "#000000"]
            : ["#5D9DFF", "#4E89B9", "#2563EB"]
        }
        style={styles.header}
      >
        <TouchableOpacity
          onPress={() => navigation.goBack()}
        >
          <Ionicons
            name="arrow-back"
            size={24}
            color="#FFFFFF"
          />
        </TouchableOpacity>

        <Text style={styles.title}>
          Contact Support
        </Text>
      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.content}
      >
        <Text
          style={[
            styles.label,
            { color: colors.text },
          ]}
        >
          Subject
        </Text>

        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: colors.card,
              borderColor: colors.border,
              color: colors.text,
            },
          ]}
          placeholder="Enter subject"
          placeholderTextColor={colors.subText}
          value={subject}
          onChangeText={setSubject}
        />

        <Text
          style={[
            styles.label,
            { color: colors.text },
          ]}
        >
          Message
        </Text>

        <TextInput
          style={[
            styles.textArea,
            {
              backgroundColor: colors.card,
              borderColor: colors.border,
              color: colors.text,
            },
          ]}
          placeholder="Describe your issue..."
          placeholderTextColor={colors.subText}
          multiline
          numberOfLines={7}
          textAlignVertical="top"
          value={message}
          onChangeText={setMessage}
        />

        <TouchableOpacity
          style={[
            styles.button,
            {
              backgroundColor: colors.primary,
            },
          ]}
          onPress={sendMessage}
          disabled={loading}
        >
          <Ionicons
            name="send"
            size={20}
            color="#FFFFFF"
          />

          <Text style={styles.buttonText}>
            {loading
              ? "Sending..."
              : "Send Message"}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  header: {
    paddingTop: 50,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },

  title: {
    color: "#FFFFFF",
    fontSize: 24,
    fontWeight: "700",
    marginTop: 18,
  },

  content: {
    padding: 20,
  },

  label: {
    marginBottom: 8,
    fontSize: 16,
    fontWeight: "700",
  },

  input: {
    borderRadius: 15,
    padding: 15,
    marginBottom: 20,
    borderWidth: 1,
    fontSize: 15,
  },

  textArea: {
    borderRadius: 15,
    padding: 15,
    height: 180,
    borderWidth: 1,
    fontSize: 15,
  },

  button: {
    marginTop: 30,
    height: 56,
    borderRadius: 28,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
  },

  buttonText: {
    color: "#FFFFFF",
    marginLeft: 10,
    fontSize: 17,
    fontWeight: "700",
  },
});