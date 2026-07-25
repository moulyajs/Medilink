import { createNativeStackNavigator } from "@react-navigation/native-stack";

import SplashScreen from "../screens/SplashScreen";

// Onboarding
import Onboarding1 from "../screens/onboarding/Onboarding1";
import Onboarding2 from "../screens/onboarding/Onboarding2";
import Onboarding3 from "../screens/onboarding/Onboarding3";

// Authentication
import LoginScreen from "../screens/auth/LoginScreen";
import SignupScreen from "../screens/auth/SignupScreen";
import ForgotPasswordScreen from "../screens/auth/ForgotPasswordScreen";
import VerifyOTPScreen from "../screens/auth/VerifyOTPScreen";
import ResetPasswordScreen from "../screens/auth/ResetPasswordScreen";

// Dashboard
import Dashboard from "../screens/dashboard/Dashboard";

// Upload
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

// Chatbot
import ChatHome from "../screens/chatbot/ChatHome";
import ChatScreen from "../screens/chatbot/ChatScreen";

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Splash"
      screenOptions={{
        headerShown: false,
      }}
    >
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

      {/* Profile */}
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
      />
      <Stack.Screen
        name="EditProfile"
        component={EditProfileScreen}
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
    </Stack.Navigator>
  );
}