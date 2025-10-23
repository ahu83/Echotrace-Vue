import axios from "axios";

const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || "http://127.0.0.1:5000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;