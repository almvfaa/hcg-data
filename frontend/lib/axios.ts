// frontend/lib/axios.ts
import axios from 'axios';

/**
 * A centralized and pre-configured Axios instance for making API requests.
 */
const apiClient = axios.create({
  /**
   * The base URL for all API requests.
   * It's recommended to set this in your environment variables.
   */
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  
  /**
   * Default headers for all requests.
   */
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Axios interceptor to handle successful responses.
 * This function unwraps the response to directly return the data.
 */
apiClient.interceptors.response.use(
  (response) => response.data,
  /**
   * Axios interceptor to handle errors globally.
   * This function logs the error and rejects the promise with structured error information.
   */
  (error) => {
    // Log the error for debugging purposes
    console.error(
      'API Error:',
      error.response?.data || error.message
    );
    
    // Reject the promise so that component-level .catch() can handle it
    return Promise.reject(error.response?.data || error);
  }
);

/**
 * In a real-world application, you would add an interceptor
 * to dynamically attach the authentication token to every request.
 *
 * apiClient.interceptors.request.use(config => {
 *   const token = localStorage.getItem('authToken');
 *   if (token) {
 *     config.headers.Authorization = `Bearer ${token}`;
 *   }
 *   return config;
 * });
 */

export default apiClient;
