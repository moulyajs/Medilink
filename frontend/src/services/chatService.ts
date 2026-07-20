import api from "./api";

export async function createSession() {
  const response = await api.post("/chat/session");
  return response.data;
}

export async function getSessions() {
  const response = await api.get("/chat/sessions");
  return response.data;
}

export async function getSession(sessionId: string) {
  const response = await api.get(`/chat/session/${sessionId}`);
  return response.data;
}
export async function deleteSession(sessionId: string) {
  await api.delete(`/chat/session/${sessionId}`);
}
export async function sendMessage(
  sessionId: string,
  query: string
) {
  const response = await api.post(
    `/chat/session/${sessionId}/message`,
    {
      query,
    }
  );

  return response.data;
}