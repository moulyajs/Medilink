import axios from "axios";
import { getToken } from "../utils/storage";

const api = axios.create({
  baseURL: "http://192.168.0.101:8000",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

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

export default api;