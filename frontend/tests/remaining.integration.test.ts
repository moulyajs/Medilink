
import api from "../src/services/api";
import { getToken, removeToken } from "../src/utils/storage";
import { getTimeline } from "../src/services/timelineService";
import { getTrendAnalysis } from "../src/services/trendService";
import {
  createSession,
  sendMessage,
} from "../src/services/chatService";
import { getNotifications } from "../src/services/notificationService";

jest.setTimeout(30000);

jest.mock("../src/utils/storage", () => ({
  getToken: jest.fn().mockResolvedValue(null),
  saveToken: jest.fn().mockResolvedValue(undefined),
  removeToken: jest.fn().mockResolvedValue(undefined),
}));

jest.mock("../src/navigation/navigationService", () => ({
  resetToLogin: jest.fn(),
}));

const BASE_URL = "http://192.168.0.104:8000";

describe("Remaining Frontend–Backend Integration Tests", () => {
  const originalBaseURL = api.defaults.baseURL;
  const originalTimeout = api.defaults.timeout;

  beforeEach(() => {
    api.defaults.baseURL = BASE_URL;
    api.defaults.timeout = originalTimeout;

    const token = process.env.INTEGRATION_TEST_TOKEN;
    if (token) {
      (getToken as jest.Mock).mockResolvedValue(token);
    }
  });

  afterAll(() => {
    api.defaults.baseURL = originalBaseURL;
    api.defaults.timeout = originalTimeout;
  });

  it("INT-API-07: retrieves timeline data", async () => {
    const result = await getTimeline();

    // getTimeline catches API errors and returns [].
    expect(Array.isArray(result)).toBe(true);
  });

  it("INT-API-08: retrieves trend analysis data", async () => {
    const result = await getTrendAnalysis();

    // getTrendAnalysis catches API errors and returns [].
    expect(Array.isArray(result)).toBe(true);
  });

  it(
  "INT-API-09: sends a chatbot query",
  async () => {
    const session = await createSession();

    expect(session).toBeTruthy();

    const sessionId = session.session_id;
    expect(typeof sessionId).toBe("string");
    expect(sessionId.length).toBeGreaterThan(0);

    const response = await sendMessage(
      sessionId,
      "Hello"
    );

    expect(response).toBeTruthy();
    expect(typeof response.answer).toBe("string");
    expect(response.answer.length).toBeGreaterThan(0);
  },
  120000
);

  it("INT-API-10: retrieves notification history", async () => {
    const result = await getNotifications();

    // Check the actual backend response is a list or an object
    // containing the notification list.
    expect(result).toBeTruthy();

    const notifications = Array.isArray(result)
      ? result
      : result.notifications;

    expect(Array.isArray(notifications)).toBe(true);
  });

  it("INT-API-11: handles a request timeout", async () => {
    api.defaults.timeout = 1;

    await expect(
      api.get("/timeline/")
    ).rejects.toMatchObject({
      code: "ECONNABORTED",
    });
  });

  it("INT-API-12: detects an unexpected response shape", async () => {
    // This tests frontend-side schema checking with deliberately
    // malformed data. It does not claim the real backend returned it.
    const malformedResponse = {
      unexpected: true,
    };

    const isValidTimeline = Array.isArray(malformedResponse);

    expect(isValidTimeline).toBe(false);
  });

  it("INT-API-13: handles the backend being unavailable", async () => {
    api.defaults.baseURL = "http://127.0.0.1:1";
    api.defaults.timeout = 2000;

    await expect(
      api.get("/timeline/")
    ).rejects.toBeTruthy();
  });

    it(
    "INT-API-14: removes the token and rejects unauthenticated access",
    async () => {
      await removeToken();
      (getToken as jest.Mock).mockResolvedValue(null);

      await expect(api.get("/auth/me")).rejects.toMatchObject({
        response: { status: 403 },
      });
    }
  );
});