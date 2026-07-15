import React from "react";
import {
  View,
  StyleSheet,
  TouchableOpacity,
  Image,
  Text,
  Dimensions,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

const { width } = Dimensions.get("window");

type Props = {
  image?: string;
  onPress: () => void;
};

export default function ProfileImagePicker({
  image,
  onPress,
}: Props) {

  return (

    <View style={styles.container}>

      {/* Avatar */}

      <View style={styles.outerCircle}>

        <View style={styles.innerCircle}>

          {image ? (

            <Image
              source={{ uri: image }}
              style={styles.image}
            />

          ) : (

            <Ionicons
              name="person"
              size={width > 900 ? 70 : 55}
              color="#FFFFFF"
            />

          )}

        </View>

      </View>

      {/* Camera Button */}

      <TouchableOpacity
        activeOpacity={0.9}
        style={styles.cameraButton}
        onPress={onPress}
      >

        <Ionicons
          name="camera"
          size={20}
          color="#FFFFFF"
        />

      </TouchableOpacity>

      {/* Hint */}

      <Text style={styles.hint}>
        Tap to change profile photo
      </Text>

    </View>

  );

}

const styles = StyleSheet.create({

  container:{

    alignItems:"center",

    marginBottom:35,

  },

  outerCircle:{

    width:150,

    height:150,

    borderRadius:75,

    backgroundColor:"#DCEEFF",

    justifyContent:"center",

    alignItems:"center",

    shadowColor:"#2563EB",

    shadowOpacity:.20,

    shadowRadius:18,

    elevation:8,

  },

  innerCircle:{

    width:132,

    height:132,

    borderRadius:66,

    backgroundColor:"#4E89B9",

    justifyContent:"center",

    alignItems:"center",

    overflow:"hidden",

  },

  image:{

    width:"100%",

    height:"100%",

  },

  cameraButton:{

    position:"absolute",

    right:width>900 ? 260 : 105,

    bottom:35,

    width:42,

    height:42,

    borderRadius:21,

    backgroundColor:"#2563EB",

    justifyContent:"center",

    alignItems:"center",

    borderWidth:3,

    borderColor:"#FFFFFF",

  },

  hint:{

    marginTop:18,

    fontSize:14,

    color:"#64748B",

    fontWeight:"600",

  },

});