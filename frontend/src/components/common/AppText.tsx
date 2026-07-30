import React from "react";
import {
  Text,
  StyleSheet,
  TextStyle,
} from "react-native";

import { useTheme } from "../../theme/ThemeContext";

type Props = {
  children: React.ReactNode;
  style?: TextStyle | TextStyle[];
};

export default function AppText({
  children,
  style,
}: Props) {

  const { colors } = useTheme();

  return (
    <Text
      style={[
        styles.text,
        {
          color: colors.text,
        },
        style,
      ]}
    >
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({

  text: {

    fontSize: 16,

  },

});