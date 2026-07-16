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

export default function ContactSupportScreen() {

  const navigation = useNavigation<any>();

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

    <SafeAreaView style={styles.container}>

      <LinearGradient
        colors={["#5D9DFF", "#4E89B9", "#2563EB"]}
        style={styles.header}
      >

        <TouchableOpacity
          onPress={() => navigation.goBack()}
        >

          <Ionicons
            name="arrow-back"
            size={24}
            color="#FFF"
          />

        </TouchableOpacity>

        <Text style={styles.title}>
          Contact Support
        </Text>

      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.content}
      >

        <Text style={styles.label}>
          Subject
        </Text>

        <TextInput
          style={styles.input}
          placeholder="Enter subject"
          value={subject}
          onChangeText={setSubject}
        />

        <Text style={styles.label}>
          Message
        </Text>

        <TextInput
          style={styles.textArea}
          placeholder="Describe your issue..."
          multiline
          numberOfLines={7}
          textAlignVertical="top"
          value={message}
          onChangeText={setMessage}
        />

        <TouchableOpacity
          style={styles.button}
          onPress={sendMessage}
          disabled={loading}
        >

          <Ionicons
            name="send"
            size={20}
            color="#FFF"
          />

          <Text style={styles.buttonText}>
            {loading ? "Sending..." : "Send Message"}
          </Text>

        </TouchableOpacity>

      </ScrollView>

    </SafeAreaView>

  );

}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: "#F5F8FC",
  },

  header: {
    paddingTop: 50,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },

  title: {
    color: "#FFF",
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
    color: "#1E293B",
  },

  input: {
    backgroundColor: "#FFF",
    borderRadius: 15,
    padding: 15,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  textArea: {
    backgroundColor: "#FFF",
    borderRadius: 15,
    padding: 15,
    height: 180,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },

  button: {
    marginTop: 30,
    height: 56,
    backgroundColor: "#2563EB",
    borderRadius: 28,
    justifyContent: "center",
    alignItems: "center",
    flexDirection: "row",
  },

  buttonText: {
    color: "#FFF",
    marginLeft: 10,
    fontSize: 17,
    fontWeight: "700",
  },

});