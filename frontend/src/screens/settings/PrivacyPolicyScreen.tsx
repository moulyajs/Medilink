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

export default function PrivacyPolicyScreen() {

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
          Privacy Policy
        </Text>

      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.content}
      >

        <Text style={styles.heading}>
          Medilink Privacy Policy
        </Text>

        <Text style={styles.paragraph}>
          Your privacy is extremely important to us.
          Medilink is committed to protecting your
          personal and medical information using
          industry-standard security practices.
        </Text>

        <Text style={styles.subHeading}>
          1. Information We Collect
        </Text>

        <Text style={styles.paragraph}>
          • Personal details (name, email, phone){'\n'}
          • Medical reports uploaded by you{'\n'}
          • AI chatbot interactions{'\n'}
          • App usage information
        </Text>

        <Text style={styles.subHeading}>
          2. How We Use Your Data
        </Text>

        <Text style={styles.paragraph}>
          Your data is used to provide personalized
          health insights, maintain your medical
          records, improve AI recommendations,
          and enhance the overall Medilink experience.
        </Text>

        <Text style={styles.subHeading}>
          3. Data Security
        </Text>

        <Text style={styles.paragraph}>
          All sensitive information is encrypted
          during transmission and storage. Access
          to medical records is restricted to
          authorized users only.
        </Text>

        <Text style={styles.subHeading}>
          4. Third-Party Services
        </Text>

        <Text style={styles.paragraph}>
          Medilink does not sell your personal
          information. Third-party services are
          used only when necessary to provide
          essential application features.
        </Text>

        <Text style={styles.subHeading}>
          5. Your Rights
        </Text>

        <Text style={styles.paragraph}>
          You may access, update, or delete your
          personal information at any time.
          You may also request permanent deletion
          of your account and associated records.
        </Text>

        <Text style={styles.subHeading}>
          6. Contact Us
        </Text>

        <Text style={styles.paragraph}>
          If you have any questions regarding this
          Privacy Policy, please contact the
          Medilink Support Team through the
          Contact Support page.
        </Text>

      </ScrollView>

    </SafeAreaView>

  );

}

const styles = StyleSheet.create({

  container:{
    flex:1,
    backgroundColor:"#F5F8FC",
  },

  header:{
    paddingTop:50,
    paddingBottom:30,
    paddingHorizontal:20,
  },

  title:{
    color:"#FFF",
    fontSize:24,
    fontWeight:"700",
    marginTop:18,
  },

  content:{
    padding:20,
  },

  heading:{
    fontSize:24,
    fontWeight:"700",
    color:"#0F172A",
    marginBottom:20,
  },

  subHeading:{
    marginTop:18,
    marginBottom:8,
    fontSize:18,
    fontWeight:"700",
    color:"#2563EB",
  },

  paragraph:{
    fontSize:15,
    lineHeight:24,
    color:"#475569",
  },

});