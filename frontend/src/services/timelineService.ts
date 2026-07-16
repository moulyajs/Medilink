import axios from "axios";
import { TimelineItem } from "../types/timeline";

// Change this if using Android emulator or physical phone
const API = "http://127.0.0.1:8000";

export const getTimeline = async (
  patientId: string
): Promise<TimelineItem[]> => {
  try {
    const response = await axios.get(
      `${API}/timeline/${patientId.trim()}`
    );

    return response.data;
  } catch (error) {
    console.error("Timeline API Error:", error);
    return [];
  }
};

export const getDocumentUrl = (
    documentId: string
) => {
    return `${API}/document/${documentId}`;
};