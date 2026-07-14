import { TrendData } from "../types/trend";

const BASE_URL = "http://127.0.0.1:8000";

// If testing on Android Emulator use:
// const BASE_URL = "http://10.0.2.2:8000";

// If testing on physical phone use:
// const BASE_URL = "http://YOUR_PC_IP:8000";

export async function getTrendAnalysis(
  patientId: string
): Promise<TrendData[]> {
  try {
    const response = await fetch(
      `${BASE_URL}/trend-analysis/${patientId}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(
        `Server returned ${response.status}`
      );
    }

    const data: TrendData[] = await response.json();

    return data;
  } catch (error) {
    console.error("Trend API Error:", error);
    return [];
  }
}