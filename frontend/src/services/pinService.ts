import * as SecureStore from "expo-secure-store";

const PIN_KEY = "app_pin";

export const savePin = async (pin: string) => {
  await SecureStore.setItemAsync(
    PIN_KEY,
    pin
  );
};

export const getPin = async () => {
  return await SecureStore.getItemAsync(
    PIN_KEY
  );
};

export const verifyPin = async (
  enteredPin: string
) => {
  const savedPin =
    await getPin();

  return savedPin === enteredPin;
};

export const isPinEnabled = async () => {
  const pin =
    await getPin();

  return pin !== null;
};

export const disablePin = async () => {
  await SecureStore.deleteItemAsync(
    PIN_KEY
  );
};