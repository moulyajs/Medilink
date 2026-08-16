import axios from "axios";
import {
  getToken,
  removeToken,
} from "../utils/storage";
import {
  resetToLogin,
} from "../navigation/navigationService";

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 300000,
});

// =====================================================
// ATTACH JWT
// =====================================================

api.interceptors.request.use(
  async (config) => {

    const token = await getToken();

    console.log(
      "API REQUEST:",
      config.method?.toUpperCase(),
      config.url
    );

    console.log(
      "JWT EXISTS:",
      !!token
    );

    if (token) {

      config.headers =
        config.headers || {};

      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);

// =====================================================
// RESPONSE INTERCEPTOR
// =====================================================

api.interceptors.response.use(
  (response) => response,

  async (error) => {

    console.error(
      "API ERROR:",
      error?.config?.url
    );

    console.error(
      "STATUS:",
      error?.response?.status
    );

    if (
      error.response?.status === 401
    ) {

      console.log(
        "401 Unauthorized"
      );

      await removeToken();

      resetToLogin();
    }

    return Promise.reject(error);
  }
);

export default api;