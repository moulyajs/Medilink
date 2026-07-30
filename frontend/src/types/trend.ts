export interface TrendHistory {
  date: string;
  value: number;
}

export interface TrendData {
  test_name: string;
  latest_value: number;
  delta: number | null;
  slope: number | null;
  trend: string;
  status: string;
  data_points: number;
  history: TrendHistory[];
}