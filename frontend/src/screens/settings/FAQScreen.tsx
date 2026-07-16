import React, { useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

const faqData = [
  {
    question: "How do I upload a medical report?",
    answer:
      "Go to Dashboard → Upload Report and select a PDF or image from your device.",
  },
  {
    question: "How secure is my medical data?",
    answer:
      "Your medical records are securely stored and encrypted to protect your privacy.",
  },
  {
    question: "Can I edit my profile information?",
    answer:
      "Yes. Open Profile → Edit Profile and update your personal details.",
  },
  {
    question: "How do I reset my password?",
    answer:
      "Use the Forgot Password option on the login screen.",
  },
  {
    question: "How does AI Health Insights work?",
    answer:
      "Our AI analyzes your uploaded reports and provides trends and health insights.",
  },
];

export default function FAQScreen() {

  const navigation = useNavigation<any>();

  const [expanded, setExpanded] = useState<number | null>(null);

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

        <Text style={styles.headerTitle}>
          Frequently Asked Questions
        </Text>

      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.content}
      >

        {faqData.map((item, index) => (

          <View
            key={index}
            style={styles.card}
          >

            <TouchableOpacity
              style={styles.row}
              onPress={() =>
                setExpanded(
                  expanded === index ? null : index
                )
              }
            >

              <Text style={styles.question}>
                {item.question}
              </Text>

              <Ionicons
                name={
                  expanded === index
                    ? "chevron-up"
                    : "chevron-down"
                }
                size={22}
                color="#2563EB"
              />

            </TouchableOpacity>

            {expanded === index && (

              <Text style={styles.answer}>
                {item.answer}
              </Text>

            )}

          </View>

        ))}

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
    paddingHorizontal: 20,
    paddingBottom: 30,
  },

  headerTitle: {
    color: "#FFF",
    fontSize: 24,
    fontWeight: "700",
    marginTop: 20,
  },

  content: {
    padding: 20,
  },

  card: {
    backgroundColor: "#FFF",
    borderRadius: 18,
    marginBottom: 15,
    padding: 18,

    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 4,
  },

  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  question: {
    flex: 1,
    fontSize: 16,
    fontWeight: "700",
    color: "#1E293B",
    marginRight: 10,
  },

  answer: {
    marginTop: 15,
    color: "#64748B",
    lineHeight: 22,
    fontSize: 15,
  },
});