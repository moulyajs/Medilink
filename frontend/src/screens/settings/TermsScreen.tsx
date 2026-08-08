import React from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

export default function TermsScreen() {

  const navigation = useNavigation<any>();

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
          Terms & Conditions
        </Text>

      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.content}
      >

        <Text style={styles.heading}>
          Medilink Terms & Conditions
        </Text>

        <Text style={styles.paragraph}>
          Welcome to Medilink. By using this application,
          you agree to comply with these terms and
          conditions.
        </Text>

        <Text style={styles.subHeading}>
          1. Medical Disclaimer
        </Text>

        <Text style={styles.paragraph}>
          Medilink provides AI-assisted insights and health
          record management. It is not a substitute for
          professional medical advice, diagnosis, or
          treatment.
        </Text>

        <Text style={styles.subHeading}>
          2. User Responsibilities
        </Text>

        <Text style={styles.paragraph}>
          You are responsible for maintaining the accuracy
          of your health information and protecting your
          account credentials.
        </Text>

        <Text style={styles.subHeading}>
          3. Privacy
        </Text>

        <Text style={styles.paragraph}>
          Your health information is securely stored and
          encrypted. We never share your personal medical
          data without your consent unless required by law.
        </Text>

        <Text style={styles.subHeading}>
          4. AI Recommendations
        </Text>

        <Text style={styles.paragraph}>
          AI-generated recommendations are for educational
          purposes only and should always be verified by a
          qualified healthcare professional.
        </Text>

        <Text style={styles.subHeading}>
          5. Updates
        </Text>

        <Text style={styles.paragraph}>
          These terms may be updated periodically. Continued
          use of the application indicates acceptance of the
          revised terms.
        </Text>

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

  heading: {
    fontSize: 24,
    fontWeight: "700",
    color: "#0F172A",
    marginBottom: 20,
  },

  subHeading: {
    marginTop: 18,
    marginBottom: 8,
    fontSize: 18,
    fontWeight: "700",
    color: "#2563EB",
  },

  paragraph: {
    fontSize: 15,
    lineHeight: 24,
    color: "#475569",
  },

});