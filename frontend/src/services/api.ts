import axios from "axios";
import { getToken, removeToken } from "../utils/storage";
import { resetToLogin } from "../navigation/navigationService";
const api = axios.create({
  baseURL: "http://192.168.0.107:8000",
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT to every request
api.interceptors.request.use(
  async (config) => {
    const token = await getToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Logout automatically if session is invalid
// Logout automatically if session is invalid
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    if (error.response?.status === 401) {
      console.log("401 Unauthorized");

      await removeToken();

      resetToLogin();
    }

    return Promise.reject(error);
  }
);

export default api;