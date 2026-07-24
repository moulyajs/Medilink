import api from "./api";
import { TrendData } from "../types/trend";

export async function getTrendAnalysis(): Promise<TrendData[]> {
  try {
    const response = await api.get<TrendData[]>("/trend/trend-analysis");
    return response.data;
  } catch (error) {
    console.error("Trend API Error:", error);
    return [];
  }
}