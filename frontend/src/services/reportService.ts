import { Platform } from "react-native";
import api from "./api";

/* -----------------------------
   Types
------------------------------ */

export interface ReportListItem {
  document_id: string;
  document_type: string;
  upload_date: string;
  status: string;
  lab_count: number;
}

export interface ReportDetail {
  document_id: string;
  document_type: string;
  upload_date: string;
  status: string;
  lab_values: any[];
}

/* -----------------------------
   Upload Report
------------------------------ */

export async function uploadReport(file: any) {
  const formData = new FormData();

  if (Platform.OS === "web" && file.file) {
    formData.append("file", file.file);
  } else {
    formData.append(
      "file",
      {
        uri: file.uri,
        name: file.fileName || file.name || "upload.jpg",
        type: file.mimeType || file.type || "image/jpeg",
      } as any
    );
  }

  const response = await api.post("/reports/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

/* -----------------------------
   Get Reports List
------------------------------ */

export async function getReports(): Promise<ReportListItem[]> {
  const response = await api.get("/reports/list");
  return response.data;
}

/* -----------------------------
   Get Report Details
------------------------------ */

export async function getReportById(
  documentId: string
): Promise<ReportDetail> {
  const response = await api.get(`/reports/${documentId}`);
  return response.data;
}

/* -----------------------------
   Confirm Report
------------------------------ */

export async function confirmReport(
  tempFileId: string,
  labValues: any[]
) {
  const response = await api.post("/reports/confirm", {
    temp_file_id: tempFileId,
    lab_values: labValues,
  });

  return response.data;
}