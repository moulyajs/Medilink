import api from "./api";

export interface LoginRequest {
  email: string;
  password: string;

  device_name: string | null;
  device_os: string;
  device_type: string;
}

export interface SignupRequest {
  name: string;
  email: string;
  password: string;
  phone: string;
  dob: string;
  gender: string;
}

export const signup = (data: SignupRequest) =>
  api.post("/auth/signup", data);


export const login = async (data: any) => {
  console.log("REQUEST BODY:", JSON.stringify(data, null, 2));

  const response = await api.post("/auth/login", data);

  return response;
};

export const forgotPassword = (data: {
  email: string;
}) =>
  api.post("/auth/forgot-password", data);

export const verifyOTP = (data: {
  email: string;
  otp: string;
}) =>
  api.post("/auth/verify-reset-otp", data);

export const resetPassword = (data: {
  email: string;
  otp: string;
  new_password: string;
}) =>
  api.post("/auth/reset-password", data);

export const getCurrentPatient = () =>
  api.get("/auth/me");