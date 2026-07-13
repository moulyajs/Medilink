import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import ChatHome from "../screens/chatbot/ChatHome";
import ChatScreen from "../screens/chatbot/ChatScreen";

export type RootStackParamList = {
  ChatHome: undefined;
  ChatScreen: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="ChatHome"
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen
          name="ChatHome"
          component={ChatHome}
        />

        <Stack.Screen
          name="ChatScreen"
          component={ChatScreen}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}