import { NavigationContainer } from "@react-navigation/native";
import AppNavigator from "./src/navigation/AppNavigator";
import { navigationRef } from "./src/navigation/navigationService";
import { ThemeProvider } from "./src/theme/ThemeContext";
export default function App() {
  return (
     <ThemeProvider>
    <NavigationContainer ref={navigationRef}>
      <AppNavigator />
    </NavigationContainer>
     </ThemeProvider>
  );
}