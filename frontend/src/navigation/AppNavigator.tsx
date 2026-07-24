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
import TrendScreen from "../screens/trends/TrendScreen";
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
import CreatePinScreen from "../screens/settings/CreatePinScreen";
import PinLoginScreen from "../screens/auth/PinLoginScreen";
import AboutMedilinkScreen from "../screens/settings/AboutMedilinkScreen";
import ConnectedDevicesScreen from "../screens/settings/ConnectedDevicesScreen";
//import NotificationSettingsScreen from "../screens/settings/NotificationSettingsScreen";
import PermissionsScreen from "../screens/settings/PermissionsScreen";
import EncryptionStatusScreen from "../screens/settings/EncryptionStatusScreen";
import UploadReportScreen from "../screens/upload/UploadReportScreen";
import UploadProgressScreen from "../screens/upload/UploadProgressScreen";
import UploadCompletedScreen from "../screens/upload/UploadCompletedScreen";
import AnomalyScreen from "../screens/anomalies/AnomalyScreen";
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
  name="CreatePin"
  component={CreatePinScreen}
/>
<Stack.Screen
    name="PinLogin"
    component={PinLoginScreen}
/>
<Stack.Screen
  name="ConnectedDevices"
  component={ConnectedDevicesScreen}
/>

      <Stack.Screen
  name="Dashboard"
  component={Dashboard}
/>
<Stack.Screen
  name="UploadReport"
  component={UploadReportScreen}
/>
<Stack.Screen
    name="UploadProgress"
    component={UploadProgressScreen}
/>

<Stack.Screen
    name="UploadCompleted"
    component={UploadCompletedScreen}
/>
      <Stack.Screen
        name="ChatHome"
        component={ChatHome}
      />
<Stack.Screen
  name="AboutMedilink"
  component={AboutMedilinkScreen}
/>
      <Stack.Screen
        name="ChatScreen"
        component={ChatScreen}
      />
      <Stack.Screen
  name="Permissions"
  component={PermissionsScreen}
/>

<Stack.Screen
  name="EncryptionStatus"
  component={EncryptionStatusScreen}
/>
      <Stack.Screen
        name="Trend"
        component={TrendScreen}
      />
      <Stack.Screen
  name="Anomaly"
  component={AnomalyScreen}
/>
    </Stack.Navigator>
    
   
    
  );
}