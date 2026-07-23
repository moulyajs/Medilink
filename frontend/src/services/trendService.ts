import { TrendData } from "../types/trend";

const BASE_URL = "http://127.0.0.1:8000";

export async function getTrendAnalysis(
  token: string
): Promise<TrendData[]> {
  try {
    const response = await fetch(
      `${BASE_URL}/trend/trend-analysis`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data: TrendData[] = await response.json();

    return data;
  } catch (error) {
    console.error("Trend API Error:", error);
    return [];
  }
}