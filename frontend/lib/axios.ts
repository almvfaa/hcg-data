// frontend/lib/axios.ts
import axios from "axios";

// Throw an error during build if the API URL is not defined.
// This prevents deploying a broken frontend.
if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error(
    "NEXT_PUBLIC_API_URL is not defined. Please set it in your environment variables."
  );
}

const apiClient = axios.create({
  // The base URL is taken from the environment variable.
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true, // Important for sending cookies with requests
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error.response?.data || error);
  }
);

export default apiClient;
