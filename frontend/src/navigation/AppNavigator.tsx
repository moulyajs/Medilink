import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SettingsScreen from "../screens/settings/SettingsScreen";
import SplashScreen from "../screens/SplashScreen";

// Onboarding
import Onboarding1 from "../screens/onboarding/Onboarding1";
import Onboarding2 from "../screens/onboarding/Onboarding2";
import Onboarding3 from "../screens/onboarding/Onboarding3";

// Authentication
import LoginScreen from "../screens/auth/LoginScreen";
import ReportIssueScreen from "../screens/settings/ReportIssueScreen";
import TrendScreen from "../screens/trends/TrendScreen";
import SignupScreen from "../screens/auth/SignupScreen";
import ForgotPasswordScreen from "../screens/auth/ForgotPasswordScreen";
import VerifyOTPScreen from "../screens/auth/VerifyOTPScreen";
import ResetPasswordScreen from "../screens/auth/ResetPasswordScreen";

// Dashboard
import Dashboard from "../screens/dashboard/Dashboard";

// Upload
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
import NotificationSettingsScreen from "../screens/settings/NotificationSettingsScreen";
import PermissionsScreen from "../screens/settings/PermissionsScreen";
import EncryptionStatusScreen from "../screens/settings/EncryptionStatusScreen";
import UploadReportScreen from "../screens/upload/UploadReportScreen";
import UploadProgressScreen from "../screens/upload/UploadProgressScreen";
import OCRPreviewScreen from "../screens/upload/OCRPreviewScreen";
import UploadCompletedScreen from "../screens/upload/UploadCompletedScreen";

// Reports
import ReportsList from "../screens/reports/ReportsList";
import ReportDetails from "../screens/reports/ReportDetails";

// Profile
import ProfileScreen from "../screens/profile/ProfileScreen";
import EditProfileScreen from "../screens/profile/EditProfileScreen";

//timeline
import TimelineScreen from "../screens/timeline/TimelineScreen";

// Chatbot
import ChatHome from "../screens/chatbot/ChatHome";
import ChatScreen from "../screens/chatbot/ChatScreen";

import AnomalyScreen from "../screens/anomalies/AnomalyScreen";
import NotificationScreen from "../screens/notifications/NotificationScreen";
const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Splash"
      screenOptions={{
        headerShown: false,
      }}
    >
      {/* Profile & Settings */}
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

      {/* Splash */}
      <Stack.Screen
        name="Splash"
        component={SplashScreen}
      />

      {/* Onboarding */}
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

      {/* Authentication */}
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

      {/* Dashboard */}
      <Stack.Screen
        name="Dashboard"
        component={Dashboard}
      />

      {/* Upload */}
      <Stack.Screen
        name="UploadReport"
        component={UploadReportScreen}
      />
      <Stack.Screen
        name="UploadProgress"
        component={UploadProgressScreen}
      />
      <Stack.Screen
        name="OCRPreview"
        component={OCRPreviewScreen}
      />
      <Stack.Screen
        name="UploadCompleted"
        component={UploadCompletedScreen}
      />

      {/* Reports */}
      <Stack.Screen
        name="ReportsList"
        component={ReportsList}
      />
      <Stack.Screen
        name="ReportDetails"
        component={ReportDetails}
      />

      {/* Chatbot */}
      <Stack.Screen
        name="ChatHome"
        component={ChatHome}
      />
      <Stack.Screen
        name="ChatScreen"
        component={ChatScreen}
      />

      {/* About */}
      <Stack.Screen
        name="AboutMedilink"
        component={AboutMedilinkScreen}
      />

      {/* Security */}
      <Stack.Screen
        name="Permissions"
        component={PermissionsScreen}
      />
      <Stack.Screen
        name="EncryptionStatus"
        component={EncryptionStatusScreen}
      />

      {/* Notifications */}
      <Stack.Screen
        name="Notifications"
        component={NotificationScreen}
      />
      <Stack.Screen
        name="NotificationSettings"
        component={NotificationSettingsScreen}
      />

      <Stack.Screen
        name="Timeline"
        component={TimelineScreen}
      />


      {/* Health */}
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