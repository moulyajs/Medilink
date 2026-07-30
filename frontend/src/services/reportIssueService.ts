import api from "./api";

export interface ReportIssueRequest {
  email: string;
  category: string;
  title: string;
  description: string;
}

export const reportIssue = async (
  data: ReportIssueRequest
) => {

  const response = await api.post(
    "/support/report-issue",
    data
  );

  return response.data;

};