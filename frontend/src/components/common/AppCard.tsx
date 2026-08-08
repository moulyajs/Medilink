import React from "react";
import {
  View,
  StyleSheet,
  ViewStyle,
} from "react-native";

import { useTheme } from "../../theme/ThemeContext";

type Props = {
  children: React.ReactNode;
  style?: ViewStyle | ViewStyle[];
};

export default function AppCard({
  children,
  style,
}: Props) {

  const { colors } = useTheme();

  return (
    <View
      style={[
        styles.card,
        {
          backgroundColor: colors.card,
          borderColor: colors.border,
          shadowColor: colors.shadow,
        },
        style,
      ]}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({

  card: {

    borderRadius: 18,

    padding: 18,

    borderWidth: 1,

    shadowOpacity: 0.08,

    shadowRadius: 10,

    shadowOffset: {
      width: 0,
      height: 5,
    },

    elevation: 4,

  },

});