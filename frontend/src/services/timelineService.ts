import api from "./api";
import { TimelineItem } from "../types/timeline";

export const getTimeline = async (): Promise<TimelineItem[]> => {
  try {
    const response = await api.get("/timeline/");
    return response.data;
  } catch (error) {
    console.error("Timeline API Error:", error);
    return [];
  }
};

export const viewDocument = async (
  documentId: string
): Promise<string> => {
  try {
    console.log("VIEW DOCUMENT ID:", documentId);

    const response = await api.get(
      `/document/${documentId}`,
      {
        responseType: "blob",
      }
    );

    const blobUrl = URL.createObjectURL(
      response.data
    );

    console.log("DOCUMENT BLOB URL:", blobUrl);

    return blobUrl;

  } catch (error: any) {
    console.error(
      "Document View Error:",
      error
    );

    console.error(
      "Response:",
      error?.response
    );

    throw error;
  }
};