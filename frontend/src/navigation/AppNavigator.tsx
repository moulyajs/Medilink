import { createNativeStackNavigator } from "@react-navigation/native-stack";

import SplashScreen from "../screens/SplashScreen";

import Onboarding1 from "../screens/onboarding/Onboarding1";
import Onboarding2 from "../screens/onboarding/Onboarding2";
import Onboarding3 from "../screens/onboarding/Onboarding3";

import LoginScreen from "../screens/auth/LoginScreen";

import ChatHome from "../screens/chatbot/ChatHome";
import ChatScreen from "../screens/chatbot/ChatScreen";

import ProfileScreen from "../screens/profile/ProfileScreen";
import EditProfileScreen from "../screens/profile/EditProfileScreen";
const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Splash"
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
      />
      <Stack.Screen
  name="EditProfile"
  component={EditProfileScreen}
/>
      <Stack.Screen
        name="Splash"
        component={SplashScreen}
      />

      <Stack.Screen
        name="Onboarding1"
        component={Onboarding1}
      />

      <Stack.Screen
        name="Onboarding2"
        component={Onboarding2}
      />

      <Stack.Screen
        name="Onboarding3"
        component={Onboarding3}
      />
      
      <Stack.Screen
        name="Login"
        component={LoginScreen}
      />

      <Stack.Screen
        name="ChatHome"
        component={ChatHome}
      />

      <Stack.Screen
        name="ChatScreen"
        component={ChatScreen}
      />
    </Stack.Navigator>
  );
}