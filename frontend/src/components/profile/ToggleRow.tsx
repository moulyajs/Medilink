import React from "react";
import {
  View,
  Text,
  StyleSheet,
  Switch,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

type Props = {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  subtitle?: string;
  value: boolean;
  onValueChange: (value: boolean) => void;
};

export default function ToggleRow({
  icon,
  title,
  subtitle,
  value,
  onValueChange,
}: Props) {

  return (

    <View style={styles.container}>

      <View style={styles.leftSection}>

        <View style={styles.iconContainer}>

          <Ionicons
            name={icon}
            size={22}
            color="#2563EB"
          />

        </View>

        <View>

          <Text style={styles.title}>
            {title}
          </Text>

          {subtitle && (
            <Text style={styles.subtitle}>
              {subtitle}
            </Text>
          )}

        </View>

      </View>

      <Switch
        value={value}
        onValueChange={onValueChange}
        thumbColor="#FFFFFF"
        trackColor={{
          false: "#CBD5E1",
          true: "#2563EB",
        }}
      />

    </View>

  );

}

const styles = StyleSheet.create({

  container:{

    flexDirection:"row",

    justifyContent:"space-between",

    alignItems:"center",

    backgroundColor:"#FFFFFF",

    padding:18,

    borderRadius:16,

    marginBottom:16,

    borderWidth:1,

    borderColor:"#E2E8F0",

    shadowColor:"#000",

    shadowOpacity:.05,

    shadowRadius:8,

    elevation:4

  },

  leftSection:{

    flexDirection:"row",

    alignItems:"center",

    flex:1

  },

  iconContainer:{

    width:46,

    height:46,

    borderRadius:12,

    backgroundColor:"#EFF6FF",

    justifyContent:"center",

    alignItems:"center",

    marginRight:16

  },

  title:{

    fontSize:16,

    fontWeight:"600",

    color:"#0F172A"

  },

  subtitle:{

    marginTop:4,

    color:"#64748B",

    fontSize:13

  }

});