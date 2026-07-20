import React, { useEffect } from "react";
import { View, StyleSheet } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withRepeat,
  withSequence,
  withSpring,
  withTiming,
} from "react-native-reanimated";
import { Ionicons } from "@expo/vector-icons";

export default function AnimatedLogo() {

  const scale = useSharedValue(0.5);
  const translateY = useSharedValue(0);

  useEffect(() => {

    scale.value = withSpring(1);

    translateY.value = withRepeat(
      withSequence(
        withTiming(-8, { duration: 1500 }),
        withTiming(0, { duration: 1500 })
      ),
      -1,
      false
    );

  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { scale: scale.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <Animated.View style={[styles.outerCard, animatedStyle]}>
      <View style={styles.innerSquare}>
        <Ionicons name="add" size={34} color="white" />
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  outerCard: {
    width: 145,
    height: 145,
    borderRadius: 32,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",

    shadowColor: "#4E89B9",
    shadowOpacity: 0.22,
    shadowRadius: 22,
    shadowOffset: {
      width: 0,
      height: 10,
    },

    elevation: 10,
  },

  innerSquare: {
    width: 65,
    height: 65,
    borderRadius: 18,
    backgroundColor: "#4E89B9",
    justifyContent: "center",
    alignItems: "center",
  },
});