
import {
  signup,
  login,
  getCurrentPatient,
} from "../src/services/authService";

import { getToken } from "../src/utils/storage";

jest.setTimeout(30000);

// Mock local token storage only.
// API requests and responses remain real.
jest.mock("../src/utils/storage", () => ({
  getToken: jest.fn().mockResolvedValue(null),
  saveToken: jest.fn().mockResolvedValue(undefined),
  removeToken: jest.fn().mockResolvedValue(undefined),
}));

jest.mock("../src/navigation/navigationService", () => ({
  resetToLogin: jest.fn(),
}));

describe("Frontend–Backend Auth Integration", () => {
  const email = `frontend_int_${Date.now()}_${Math.random()
    .toString(36)
    .slice(2, 8)}@example.com`;

  const password = "TestPassword123!";

  let accessToken: string | undefined;

  it("registers a patient through the real signup API", async () => {
    const response = await signup({
      name: "Frontend Integration Patient",
      email,
      password,
      phone: "9876543210",
      dob: "2000-01-15",
      gender: "Female",
    });

    expect(response.status).toBe(201);
    expect(response.data.message).toBe(
      "Account created successfully."
    );
  });

  it("rejects duplicate registration through the real API", async () => {
    await expect(
      signup({
        name: "Frontend Integration Patient",
        email,
        password,
        phone: "9876543210",
        dob: "2000-01-15",
        gender: "Female",
      })
    ).rejects.toMatchObject({
      response: {
        status: 400,
        data: {
          detail: "Email already registered.",
        },
      },
    });
  });

  it("logs in through the real API and receives a token", async () => {
    const response = await login({
      email,
      password,
      device_name: "Integration Test Device",
      device_os: "Test OS",
      device_type: "1",
    });

    expect(response.status).toBe(200);
    expect(response.data.access_token).toBeTruthy();

    accessToken = response.data.access_token;
  });

  it("uses the login token to retrieve the current patient", async () => {
    expect(accessToken).toBeTruthy();

    (getToken as jest.Mock).mockResolvedValue(accessToken);

    const response = await getCurrentPatient();

    expect(response.status).toBe(200);
    expect(response.data).toBeTruthy();
  });
});

it("rejects an invalid JWT when retrieving the current patient", async () => {
  (getToken as jest.Mock).mockResolvedValue("invalid.integration.test.token");

  await expect(getCurrentPatient()).rejects.toMatchObject({
    response: {
      status: 401,
    },
  });
});
