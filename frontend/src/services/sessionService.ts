import api from "./api";

export interface Session {
  session_id: string;
  device_name: string;
  platform: string;
  ip_address: string;
  created_at: string;
  last_active: string;
  current: boolean;
}

export const getSessions = async (): Promise<Session[]> => {
  const response = await api.get("/sessions");
  return response.data;
};

export const logoutSession = async (
  sessionId: string
) => {
  await api.delete(`/sessions/${sessionId}`);
};

export const logoutAllSessions = async () => {
  await api.delete("/sessions");
};