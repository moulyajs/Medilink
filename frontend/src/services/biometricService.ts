import * as LocalAuthentication from "expo-local-authentication";
import * as SecureStore from "expo-secure-store";

const BIOMETRIC_KEY = "biometric_enabled";

/**
 * Check if the device supports biometrics
 */
export const isBiometricSupported = async () => {
  const compatible = await LocalAuthentication.hasHardwareAsync();
  return compatible;
};

/**
 * Check if user has enrolled fingerprint/face
 */
export const isBiometricEnrolled = async () => {
  const enrolled = await LocalAuthentication.isEnrolledAsync();
  return enrolled;
};

/**
 * Authenticate using fingerprint/Face ID
 */
export const authenticateBiometric = async () => {
  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: "Authenticate to continue",
    fallbackLabel: "Use Passcode",
    cancelLabel: "Cancel",
    disableDeviceFallback: false,
  });

  return result.success;
};

/**
 * Enable biometric login
 */
export const enableBiometric = async () => {
  await SecureStore.setItemAsync(
    BIOMETRIC_KEY,
    "true"
  );
};

/**
 * Disable biometric login
 */
export const disableBiometric = async () => {
  await SecureStore.deleteItemAsync(
    BIOMETRIC_KEY
  );
};

/**
 * Check if biometric login is enabled
 */
export const isBiometricEnabled = async () => {
  const value = await SecureStore.getItemAsync(
    BIOMETRIC_KEY
  );

  return value === "true";
};