import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SettingsScreen from "../screens/settings/SettingsScreen";
import SplashScreen from "../screens/SplashScreen";

import Onboarding1 from "../screens/onboarding/Onboarding1";
import Onboarding2 from "../screens/onboarding/Onboarding2";
import Onboarding3 from "../screens/onboarding/Onboarding3";

import LoginScreen from "../screens/auth/LoginScreen";

import ChatHome from "../screens/chatbot/ChatHome";
import ChatScreen from "../screens/chatbot/ChatScreen";
import ReportIssueScreen from "../screens/settings/ReportIssueScreen";
import ProfileScreen from "../screens/profile/ProfileScreen";
import EditProfileScreen from "../screens/profile/EditProfileScreen";
import SignupScreen from "../screens/auth/SignupScreen";
import Dashboard from "../screens/dashboard/Dashboard";
import ForgotPasswordScreen from "../screens/auth/ForgotPasswordScreen";
import VerifyOTPScreen from "../screens/auth/VerifyOTPScreen";
import ResetPasswordScreen from "../screens/auth/ResetPasswordScreen";
import PrivacySettingsScreen from "../screens/settings/PrivacySettingsScreen";
import HelpSupportScreen from "../screens/settings/HelpSupportScreen";
import ContactSupportScreen from "../screens/settings/ContactSupportScreen";
import FAQScreen from "../screens/settings/FAQScreen";
import TermsScreen from "../screens/settings/TermsScreen";
import PrivacyPolicyScreen from "../screens/settings/PrivacyPolicyScreen";
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
  name="Settings"
  component={SettingsScreen}
/>
<Stack.Screen
  name="Privacy"
  component={PrivacySettingsScreen}
/>
<Stack.Screen
  name="HelpSupport"
  component={HelpSupportScreen}
/>
<Stack.Screen
  name="FAQ"
  component={FAQScreen}
/>
<Stack.Screen
    name="ContactSupport"
    component={ContactSupportScreen}
/>
<Stack.Screen
  name="ReportIssue"
  component={ReportIssueScreen}
/>
<Stack.Screen
  name="Terms"
  component={TermsScreen}
/>
<Stack.Screen
  name="PrivacyPolicy"
  component={PrivacyPolicyScreen}
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
  name="Signup"
  component={SignupScreen}
/>
      <Stack.Screen
  name="ForgotPassword"
  component={ForgotPasswordScreen}
/>

<Stack.Screen
  name="VerifyOTP"
  component={VerifyOTPScreen}
/>

<Stack.Screen
  name="ResetPassword"
  component={ResetPasswordScreen}
/>
      <Stack.Screen
  name="Dashboard"
  component={Dashboard}
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