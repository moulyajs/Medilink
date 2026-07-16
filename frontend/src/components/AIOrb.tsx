import React, { useEffect, useRef } from "react";
import {
  View,
  StyleSheet,
  Animated,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

export default function AIOrb() {

  const pulse = useRef(new Animated.Value(1)).current;
  const rotate = useRef(new Animated.Value(0)).current;

  useEffect(() => {

    Animated.loop(

      Animated.sequence([

        Animated.timing(pulse, {
          toValue: 1.08,
          duration: 900,
          useNativeDriver: true,
        }),

        Animated.timing(pulse, {
          toValue: 1,
          duration: 900,
          useNativeDriver: true,
        }),

      ])

    ).start();

    Animated.loop(

      Animated.timing(rotate, {

        toValue: 1,

        duration: 12000,

        useNativeDriver: true,

      })

    ).start();

  }, []);

  const spin = rotate.interpolate({

    inputRange: [0, 1],

    outputRange: ["0deg", "360deg"],

  });

  return (

    <View style={styles.container}>

      {/* Outer Ring */}

      <Animated.View
        style={[
          styles.ringLarge,
          {
            transform: [{ rotate: spin }],
          },
        ]}
      />

      {/* Middle Ring */}

      <Animated.View
        style={[
          styles.ringSmall,
          {
            transform: [{ rotate: spin }],
          },
        ]}
      />

      {/* AI Orb */}

      <Animated.View
        style={[
          styles.orb,
          {
            transform: [{ scale: pulse }],
          },
        ]}
      >

        <Ionicons
          name="sparkles"
          size={34}
          color="#FFFFFF"
        />

      </Animated.View>

    </View>

  );

}

const styles = StyleSheet.create({

  container: {

    width: 230,

    height: 230,

    justifyContent: "center",

    alignItems: "center",

  },

  ringLarge: {

    position: "absolute",

    width: 200,

    height: 200,

    borderRadius: 100,

    borderWidth: 1,

    borderColor: "#CFE5F8",

  },

  ringSmall: {

    position: "absolute",

    width: 150,

    height: 150,

    borderRadius: 75,

    borderWidth: 1.5,

    borderColor: "#B8D9F3",

  },

  orb: {

    width: 88,

    height: 88,

    borderRadius: 44,

    backgroundColor: "#4E89B9",

    justifyContent: "center",

    alignItems: "center",

    shadowColor: "#4E89B9",

    shadowOpacity: 0.55,

    shadowRadius: 28,

    shadowOffset: {

      width: 0,

      height: 10,

    },

    elevation: 14,

  },

});