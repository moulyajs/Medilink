import api from "./api";

export interface SupportRequest {
  email: string;
  subject: string;
  message: string;
}

export const sendSupportMessage = async (
  data: SupportRequest
) => {

  const response = await api.post(
    "/support/contact",
    data
  );

  return response.data;

};