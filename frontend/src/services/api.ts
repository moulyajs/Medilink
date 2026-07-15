import axios from "axios";

/*
  Android Emulator  -> http://10.0.2.2:8000
  Physical Phone    -> http://YOUR_PC_IP:8000
  Web               -> http://localhost:8000
*/

const api = axios.create({
  baseURL: "http://192.168.1.4:8000",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;