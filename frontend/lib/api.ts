// frontend/lib/api.ts
import axios, { AxiosError } from 'axios';

// Assume a global toast function exists for notifications
declare function showGlobalToast(message: string): void;

/**
 * A centralized Axios instance with pre-configured interceptors
 * for authentication and global error handling.
 */
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  }
});

// --- Request Interceptor ---
// This runs before each request is sent.
apiClient.interceptors.request.use(config => {
  // Retrieve the authentication token from local storage.
  // In a real app, this might come from a state management store or secure cookie.
  const token = localStorage.getItem('authToken');
  
  // If the token exists, add it to the Authorization header.
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  return config;
}, error => {
  // Handle any errors that occur during request setup
  return Promise.reject(error);
});

// --- Response Interceptor ---
// This runs after a response is received.
apiClient.interceptors.response.use(
  // 1. First argument: a function for successful responses (status 2xx)
  response => {
    // You can process the response here before it's passed to the calling function.
    // By default, we just return it.
    return response;
  },
  // 2. Second argument: a function for error responses
  (error: AxiosError) => {
    // Check if the error has a response from the server
    if (error.response) {
      const { status } = error.response;

      // Handle 401 Unauthorized errors (e.g., expired token)
      if (status === 401) {
        console.error("Authentication error: Redirecting to login.");
        // Remove the invalid token
        localStorage.removeItem('authToken');
        // Redirect the user to the login page
        // Use a small timeout to ensure state updates or toasts can be seen
        setTimeout(() => {
          window.location.href = '/login';
        }, 500);
      }
      
      // Handle server-side errors (5xx)
      if (status >= 500) {
        console.error("Server error:", error.response.data);
        // Display a generic, user-friendly notification
        if (typeof showGlobalToast === 'function') {
          showGlobalToast('Ocurrió un error en el servidor. Por favor, intente más tarde.');
        }
      }
    } else if (error.request) {
      // The request was made but no response was received (e.g., network error)
      console.error("Network error:", error.message);
      if (typeof showGlobalToast === 'function') {
        showGlobalToast('No se pudo conectar al servidor. Verifique su conexión a internet.');
      }
    }
    
    // Reject the promise to allow component-level .catch() or useQuery's `isError` to handle it
    return Promise.reject(error);
  }
);

export default apiClient;
