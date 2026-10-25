import React from "react";
import { fireEvent, render, waitFor } from "@testing-library/react-native";
import LoginScreen from "../src/screens/auth/LoginScreen";
import { login } from "../src/services/authService";
import { saveToken, getToken } from "../src/utils/storage";

const mockReplace = jest.fn();
const mockNavigate = jest.fn();
const mockAlert = jest.fn();

// Mock the global alert() used by LoginScreen
globalThis.alert = mockAlert;

jest.mock("@react-navigation/native", () => ({
  useNavigation: () => ({
    replace: mockReplace,
    navigate: mockNavigate,
  }),
}));

jest.mock("../src/services/authService", () => ({
  login: jest.fn(),
}));

jest.mock("../src/utils/storage", () => ({
  saveToken: jest.fn(),
  getToken: jest.fn().mockResolvedValue(null),
  removeToken: jest.fn(),
}));

jest.mock("../src/services/biometricService", () => ({
  authenticateBiometric: jest.fn(),
  isBiometricEnabled: jest.fn().mockResolvedValue(false),
}));

jest.mock("expo-device", () => ({
  modelName: "Test Device",
  osName: "Test OS",
  osVersion: "1.0",
  deviceType: 1,
}));

describe("LoginScreen", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockAlert.mockClear();
    (getToken as jest.Mock).mockResolvedValue(null);
  });

  it("renders the login form", () => {
    const { getByPlaceholderText, getByText } = render(<LoginScreen />);

    expect(getByText("Welcome Back")).toBeTruthy();
    expect(getByPlaceholderText("Email")).toBeTruthy();
    expect(getByPlaceholderText("Password")).toBeTruthy();
    expect(getByText("Login")).toBeTruthy();
  });

  it("submits credentials and handles successful login", async () => {
    (login as jest.Mock).mockResolvedValue({
      data: { access_token: "test-access-token" },
    });

    const { getByPlaceholderText, getByText } = render(<LoginScreen />);

    fireEvent.changeText(
      getByPlaceholderText("Email"),
      "test@example.com"
    );
    fireEvent.changeText(
      getByPlaceholderText("Password"),
      "TestPassword123!"
    );
    fireEvent.press(getByText("Login"));

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "TestPassword123!",
        device_name: "Test Device",
        device_os: "Test OS 1.0",
        device_type: "1",
      });

      expect(saveToken).toHaveBeenCalledWith("test-access-token");
      expect(mockAlert).toHaveBeenCalledWith("Login Successful!");
      expect(mockReplace).toHaveBeenCalledWith("Dashboard");
    });
  });

  it("displays the backend error when login fails", async () => {
    (login as jest.Mock).mockRejectedValue({
      response: {
        data: { detail: "Invalid credentials" },
      },
    });

    const { getByPlaceholderText, getByText } = render(<LoginScreen />);

    fireEvent.changeText(
      getByPlaceholderText("Email"),
      "test@example.com"
    );
    fireEvent.changeText(
      getByPlaceholderText("Password"),
      "wrong-password"
    );
    fireEvent.press(getByText("Login"));

    await waitFor(() => {
      expect(mockAlert).toHaveBeenCalledWith("Invalid credentials");
    });

    expect(saveToken).not.toHaveBeenCalled();
    expect(mockReplace).not.toHaveBeenCalled();
  });
});