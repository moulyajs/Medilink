import React, { useState } from "react";
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
   View,
} from "react-native";

import { Picker } from "@react-native-picker/picker";

import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import { getProfile } from "../../services/profileService";
import { reportIssue } from "../../services/reportIssueService";

export default function ReportIssueScreen() {

  const navigation = useNavigation<any>();

  const [category, setCategory] =
    useState("Upload Issue");

  const [title, setTitle] =
    useState("");

  const [description, setDescription] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const submitIssue = async () => {

    if (
      !title.trim() ||
      !description.trim()
    ) {

      Alert.alert(
        "Missing Information",
        "Please complete all fields."
      );

      return;

    }

    try {

      setLoading(true);

      const profile =
        await getProfile();

      await reportIssue({

        email: profile.email,

        category,

        title,

        description,

      });

      Alert.alert(
        "Success",
        "Issue reported successfully."
      );

      setTitle("");
      setDescription("");

    } catch (error) {

      console.log(error);

      Alert.alert(
        "Error",
        "Unable to submit issue."
      );

    } finally {

      setLoading(false);

    }

  };

  return (

    <SafeAreaView style={styles.container}>

      <LinearGradient
        colors={["#5D9DFF","#4E89B9","#2563EB"]}
        style={styles.header}
      >

        <TouchableOpacity
          onPress={() =>
            navigation.goBack()
          }
        >

          <Ionicons
            name="arrow-back"
            size={24}
            color="#FFF"
          />

        </TouchableOpacity>

        <Text style={styles.title}>
          Report Issue
        </Text>

      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.content}
      >

        <Text style={styles.label}>
          Category
        </Text>

        <View style={styles.pickerContainer}>

          <Picker

            selectedValue={category}

            onValueChange={setCategory}

          >

            <Picker.Item
              label="Upload Issue"
              value="Upload Issue"
            />

            <Picker.Item
              label="Login Problem"
              value="Login Problem"
            />

            <Picker.Item
              label="Profile Issue"
              value="Profile Issue"
            />

            <Picker.Item
              label="AI Chatbot Issue"
              value="AI Chatbot Issue"
            />

            <Picker.Item
              label="App Crash"
              value="App Crash"
            />

            <Picker.Item
              label="Other"
              value="Other"
            />

          </Picker>

        </View>

        <Text style={styles.label}>
          Issue Title
        </Text>

        <TextInput

          style={styles.input}

          placeholder="Issue title"

          value={title}

          onChangeText={setTitle}

        />

        <Text style={styles.label}>
          Description
        </Text>

        <TextInput

          style={styles.textArea}

          placeholder="Describe the issue"

          multiline

          numberOfLines={7}

          textAlignVertical="top"

          value={description}

          onChangeText={setDescription}

        />

        <TouchableOpacity

          style={styles.button}

          onPress={submitIssue}

          disabled={loading}

        >

          <Ionicons

            name="bug"

            size={20}

            color="#FFF"

          />

          <Text style={styles.buttonText}>

            {loading
              ? "Submitting..."
              : "Submit Issue"}

          </Text>

        </TouchableOpacity>

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

  label:{
    marginBottom:8,
    fontSize:16,
    fontWeight:"700",
    color:"#1E293B",
  },

  pickerContainer:{
    backgroundColor:"#FFF",
    borderRadius:15,
    borderWidth:1,
    borderColor:"#E2E8F0",
    marginBottom:20,
  },

  input:{
    backgroundColor:"#FFF",
    borderRadius:15,
    padding:15,
    borderWidth:1,
    borderColor:"#E2E8F0",
    marginBottom:20,
  },

  textArea:{
    backgroundColor:"#FFF",
    borderRadius:15,
    padding:15,
    borderWidth:1,
    borderColor:"#E2E8F0",
    height:180,
  },

  button:{
    marginTop:30,
    height:56,
    borderRadius:28,
    backgroundColor:"#2563EB",
    justifyContent:"center",
    alignItems:"center",
    flexDirection:"row",
  },

  buttonText:{
    color:"#FFF",
    marginLeft:10,
    fontSize:17,
    fontWeight:"700",
  },

});