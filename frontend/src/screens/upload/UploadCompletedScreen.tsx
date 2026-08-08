import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

export default function UploadCompletedScreen() {
  const navigation = useNavigation<any>();

  return (
    <SafeAreaView style={styles.container}>

      <Ionicons
        name="checkmark-circle"
        size={120}
        color="#22C55E"
      />

      <Text style={styles.title}>
        Upload Complete
      </Text>

      <Text style={styles.subtitle}>
        Your report has been processed successfully.
      </Text>

      <TouchableOpacity
  style={styles.button}
  onPress={() =>
    navigation.reset({
      index: 0,
      routes: [{ name: "Dashboard" }],
    })
  }
>
  <Text style={styles.buttonText}>
    Done
  </Text>
</TouchableOpacity>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({

  container:{
    flex:1,
    justifyContent:"center",
    alignItems:"center",
    backgroundColor:"#fff",
    padding:24
  },

  title:{
    fontSize:28,
    fontWeight:"700",
    marginTop:20
  },

  subtitle:{
    marginTop:12,
    color:"#64748B",
    textAlign:"center"
  },

  button:{
    marginTop:40,
    width:"100%",
    height:52,
    backgroundColor:"#2563EB",
    justifyContent:"center",
    alignItems:"center",
    borderRadius:12
  },

  buttonText:{
    color:"#fff",
    fontSize:16,
    fontWeight:"600"
  }

});