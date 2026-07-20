import * as Notifications from "expo-notifications";
import * as Device from "expo-device";
import { Platform } from "react-native";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowBanner: true,
    shouldShowList: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export async function registerForPushNotifications() {
  if (!Device.isDevice) {
    console.log("Must use a physical device.");
    return null;
  }

  const { status: existingStatus } =
    await Notifications.getPermissionsAsync();

  let finalStatus = existingStatus;

  if (existingStatus !== "granted") {
    const { status } =
      await Notifications.requestPermissionsAsync();

    finalStatus = status;
  }

  if (finalStatus !== "granted") {
    console.log("Permission denied.");
    return null;
  }

  const token = (
    await Notifications.getExpoPushTokenAsync()
  ).data;

  console.log("Expo Push Token:", token);

  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelAsync(
      "default",
      {
        name: "default",
        importance: Notifications.AndroidImportance.MAX,
      }
    );
  }

  return token;
}