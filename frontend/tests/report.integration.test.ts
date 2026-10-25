
import { getReports } from "../src/services/reportService";
import { getToken } from "../src/utils/storage";
import { uploadReport } from "../src/services/reportService";
import {
  
  getReportById
} from "../src/services/reportService";
jest.setTimeout(30000);

jest.mock("../src/utils/storage", () => ({
  getToken: jest.fn().mockResolvedValue(null),
  saveToken: jest.fn().mockResolvedValue(undefined),
  removeToken: jest.fn().mockResolvedValue(undefined),
}));

jest.mock("../src/navigation/navigationService", () => ({
  resetToLogin: jest.fn(),
}));

describe("Frontend–Backend Report Integration", () => {
  it("INT-API-05: retrieves reports from the real backend", async () => {
    // This endpoint requires authentication.
    // Supply a valid token from a previous login.
    const token = process.env.INTEGRATION_TEST_TOKEN;

    if (!token) {
      throw new Error(
        "Set INTEGRATION_TEST_TOKEN to a valid access token before running this test."
      );
    }

    (getToken as jest.Mock).mockResolvedValue(token);

    const reports = await getReports();

    expect(Array.isArray(reports)).toBe(true);

    for (const report of reports) {
      expect(report).toEqual(
        expect.objectContaining({
          document_id: expect.any(String),
          document_type: expect.any(String),
          upload_date: expect.any(String),
          status: expect.any(String),
          lab_count: expect.any(Number),
        })
      );
    }
  });
});
it("INT-API-06: retrieves a specific report from the real backend", async () => {
  const reports = await getReports();

  // The test account may not have any reports yet.
  if (reports.length === 0) {
    console.log("No reports available; skipping report-detail assertion.");
    return;
  }

  const documentId = reports[0].document_id;
  const report = await getReportById(documentId);

  expect(report).toEqual(
    expect.objectContaining({
      document_id: documentId,
      document_type: expect.any(String),
      upload_date: expect.any(String),
      status: expect.any(String),
      lab_values: expect.any(Array),
    })
  );
});
