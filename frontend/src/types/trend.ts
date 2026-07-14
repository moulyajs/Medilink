export interface TrendHistory {
  date: string;
  value: number;
}

export interface TrendData {
  test_name: string;
  latest_value: number;
  delta: number | null;
  slope: number | null;
  trend: "Increasing" | "Decreasing" | "Stable" | "Insufficient Data";
  status: "HIGH" | "LOW" | "NORMAL";
  data_points: number;
  history: TrendHistory[];
}