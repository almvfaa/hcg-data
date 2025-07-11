// frontend/store/authStore.ts
import { create } from 'zustand';
import apiClient from '@/lib/api'; // Import the centralized api client

// --- Type Definitions ---
// It's a good practice to define the shape of your state.
// You would replace this with the actual User type from your API.
interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
  // Optional: A function to initialize state from localStorage
  hydrate: () => void;
}

/**
 * A Zustand store for managing global authentication state.
 */
export const useAuthStore = create<AuthState>((set, get) => ({
  // --- Initial State ---
  user: null,
  token: null,
  isAuthenticated: false,

  // --- Actions ---

  /**
   * Performs user login, fetches a token, and updates the state.
   * @param credentials - The user's email and password.
   */
  login: async (credentials) => {
    try {
      // Use the centralized apiClient to make the login request.
      const response = await apiClient.post<{ user: User; token: string }>('/auth/login', credentials);
      
      // Update the state with the user and token.
      set({ 
        user: response.data.user,
        token: response.data.token,
        isAuthenticated: true,
      });

      // Persist the token to localStorage.
      localStorage.setItem('authToken', response.data.token);

      // The request interceptor in `api.ts` will now automatically use this token.

    } catch (error) {
      console.error("Login failed:", error);
      // Re-throw the error so the calling component can handle it (e.g., show a toast).
      throw error;
    }
  },
  
  /**
   * Logs the user out, clearing the state and localStorage.
   */
  logout: () => {
    // Clear the state.
    set({ user: null, token: null, isAuthenticated: false });
    // Remove the token from localStorage.
    localStorage.removeItem('authToken');
    // The request interceptor will no longer find a token.
  },

  /**
   * Hydrates the store from localStorage on application load.
   * This keeps the user logged in across page refreshes.
   */
  hydrate: () => {
    try {
      const token = localStorage.getItem('authToken');
      if (token) {
        // Here, you would typically decode the JWT to get user info and check expiration.
        // For this example, we'll assume the token is valid and contains user data.
        // const decodedUser = jwt_decode(token); 
        // set({ user: decodedUser, token, isAuthenticated: true });
        
        // Simplified hydration for now:
        set({ token, isAuthenticated: true });
      }
    } catch (error) {
      console.error("Hydration failed:", error);
      // If hydration fails, ensure the user is logged out.
      get().logout();
    }
  }
}));

// Initialize the store from localStorage when the app loads.
// This should only run on the client side.
if (typeof window !== 'undefined') {
  useAuthStore.getState().hydrate();
}
