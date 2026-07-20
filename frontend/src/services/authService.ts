import api from "./api";

export const signup = (data: any) =>
  api.post("/auth/signup", data);

export const login = (data: any) =>
  api.post("/auth/login", data);

export const forgotPassword = (data: any) =>
  api.post("/auth/forgot-password", data);

export const verifyOTP = (data: any) =>
  api.post("/auth/verify-reset-otp", data);

export const resetPassword = (data: any) =>
  api.post("/auth/reset-password", data);