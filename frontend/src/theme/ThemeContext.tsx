import React, {
  createContext,
  useContext,
  useState,
} from "react";

import {
  LightTheme,
  DarkTheme,
} from "./theme";

type ThemeType = typeof LightTheme;

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