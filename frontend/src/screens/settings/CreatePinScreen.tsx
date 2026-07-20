import React, { useState } from "react";
import {
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Alert,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import { savePin } from "../../services/pinService";

export default function CreatePinScreen() {
  const navigation = useNavigation<any>();

  const [pin, setPin] = useState("");

  const pressNumber = async (number: string) => {
    if (pin.length >= 4) return;

    const newPin = pin + number;

    setPin(newPin);

    if (newPin.length === 4) {
      await savePin(newPin);

      Alert.alert(
        "Success",
        "PIN created successfully."
      );

      navigation.goBack();
    }
  };

  const deleteNumber = () => {
    setPin(pin.slice(0, -1));
  };

  return (
    <SafeAreaView style={styles.container}>

      <Ionicons
        name="lock-closed"
        size={70}
        color="#2563EB"
      />

      <Text style={styles.title}>
        Create PIN
      </Text>

      <Text style={styles.subtitle}>
        Enter a 4-digit PIN to protect your app.
      </Text>

      <View style={styles.pinContainer}>
        {[0,1,2,3].map((i) => (
          <View
            key={i}
            style={[
              styles.dot,
              pin.length > i && styles.dotFilled,
            ]}
          />
        ))}
      </View>

      <View style={styles.keypad}>
        {[
          "1","2","3",
          "4","5","6",
          "7","8","9",
          "","0","⌫",
        ].map((item,index)=>{

          if(item===""){
            return (
              <View
                key={index}
                style={styles.key}
              />
            );
          }

          return(
            <TouchableOpacity
              key={index}
              style={styles.key}
              onPress={()=>{
                if(item==="⌫"){
                  deleteNumber();
                }else{
                  pressNumber(item);
                }
              }}
            >
              <Text style={styles.keyText}>
                {item}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({

  container:{
    flex:1,
    justifyContent:"center",
    alignItems:"center",
    backgroundColor:"#F8FAFC",
    padding:20,
  },

  title:{
    fontSize:28,
    fontWeight:"700",
    marginTop:20,
  },

  subtitle:{
    color:"#64748B",
    marginTop:8,
    marginBottom:40,
    textAlign:"center",
  },

  pinContainer:{
    flexDirection:"row",
    marginBottom:40,
  },

  dot:{
    width:18,
    height:18,
    borderRadius:9,
    borderWidth:2,
    borderColor:"#CBD5E1",
    marginHorizontal:10,
  },

  dotFilled:{
    backgroundColor:"#2563EB",
    borderColor:"#2563EB",
  },

  keypad:{
    width:"100%",
    flexDirection:"row",
    flexWrap:"wrap",
    justifyContent:"center",
  },

  key:{
    width:90,
    height:70,
    justifyContent:"center",
    alignItems:"center",
    margin:8,
    borderRadius:15,
    backgroundColor:"#FFFFFF",
    elevation:3,
  },

  keyText:{
    fontSize:28,
    fontWeight:"600",
  },

});