import axios from "axios";

export async function isTokenValid() {
  const token = localStorage.getItem("token");
  if (!token) return false;

  try {
    await axios.get(`${process.env.VUE_APP_API_URL}/verify-token`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return true;
  } catch {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    return false;
  }
}