import api from "./api";

export interface Anomaly {
  test_name: string;
  current_value: number;
  personal_average: number;
  personal_min: number;
  personal_max: number;
  personal_variability: number;
  sample_count: number;
  reference_low: number | null;
  reference_high: number | null;
  unit: string | null;
  deviation: number;
  percent_change: number;
  trend: string;
  detected_at: string;
}

export const getAnomalies = async (): Promise<Anomaly[]> => {
  const response = await api.get("/anomaly/");
  return response.data;
};