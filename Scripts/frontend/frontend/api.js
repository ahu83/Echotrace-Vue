import axios from "axios";

const api = axios.create({
  baseURL: "https://setting-milwaukee-politicians-core.trycloudflare.com",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;