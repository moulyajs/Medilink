import { StyleSheet } from "react-native";
import { useTheme } from "../theme/ThemeContext";

export function useStyles() {
  const { colors } = useTheme();

  const globalStyles = StyleSheet.create({
    screen: {
      flex: 1,
      backgroundColor: colors.background,
    },

    card: {
      backgroundColor: colors.card,
    },

    title: {
      color: colors.text,
    },

    subtitle: {
      color: colors.subText,
    },

    border: {
      borderColor: colors.border,
    },

    shadow: {
      shadowColor: colors.shadow,
    },
  });

  return {
    colors,
    globalStyles,
  };
}