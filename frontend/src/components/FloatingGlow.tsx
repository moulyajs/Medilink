import React, { useEffect, useRef } from "react";
import { Animated } from "react-native";

export default function FloatingGlow({ children }: any) {

  const translateY = useRef(new Animated.Value(0)).current;

  useEffect(() => {

    Animated.loop(
      Animated.sequence([
        Animated.timing(translateY,{
          toValue:-8,
          duration:1800,
          useNativeDriver:true
        }),

        Animated.timing(translateY,{
          toValue:0,
          duration:1800,
          useNativeDriver:true
        })
      ])
    ).start();

  },[]);

  return(

    <Animated.View
      style={{
        transform:[{translateY}]
      }}
    >
      {children}
    </Animated.View>

  );
}