import React, {
  createContext,
  useContext,
  useState,
} from "react";

import {
  LightTheme,
  DarkTheme,
} from "./theme";

type ThemeType = {
  background: string;
  card: string;
  text: string;
  subText: string;
  primary: string;
  secondary: string;
  border: string;
  success: string;
  danger: string;
  icon: string;
  shadow: string;
  header: readonly string[];
};

type ThemeContextType = {
  darkMode: boolean;
  setDarkMode: (value: boolean) => void;
  colors: ThemeType;
};

const ThemeContext = createContext<ThemeContextType>({
  darkMode: false,
  setDarkMode: () => {},
  colors: LightTheme,
});

export const ThemeProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {

  const [darkMode, setDarkMode] =
    useState(false);

  const colors = darkMode
    ? DarkTheme
    : LightTheme;

  return (
    <ThemeContext.Provider
      value={{
        darkMode,
        setDarkMode,
        colors,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () =>
  useContext(ThemeContext);