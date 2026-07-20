import React from "react";
import {
  SafeAreaView,
  StyleSheet,
  ViewStyle,
} from "react-native";

import { useTheme } from "../../theme/ThemeContext";

type Props = {
  children: React.ReactNode;
  style?: ViewStyle | ViewStyle[];
};

export default function AppScreen({
  children,
  style,
}: Props) {
  const { colors } = useTheme();

  return (
    <SafeAreaView
      style={[
        styles.container,
        {
          backgroundColor: colors.background,
        },
        style,
      ]}
    >
      {children}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});