import axios from "axios";

const api = axios.create({
  baseURL: "https://trips-enables-sellers-premium.trycloudflare.com"  || "http://127.0.0.1:5000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;