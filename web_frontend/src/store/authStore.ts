import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '../api/auth';
import type { User, AuthState } from '../types';

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      // Initialize - check if stored token is valid
      initialize: async () => {
        const token = get().token;
        if (!token) {
          return;
        }
        
        // Token exists, but we need to verify it's valid
        // If any API call fails with 401, the interceptor will clear it
        try {
          // Try to make a simple API call to verify token
          // If it fails, the error interceptor will handle it
        } catch (error) {
          // Token is invalid, clear it
          set({
            user: null,
            token: null,
            isAuthenticated: false,
          });
        }
      },

      login: async (username: string, password: string) => {
        try {
          const tokenData = await authApi.login({ username, password });
          
          // Create user object (backend doesn't return user on login)
          const user: User = {
            id: 0, // Will be populated when needed
            username,
          };
          
          // Zustand persist middleware will automatically save to localStorage
          set({
            token: tokenData.access_token,
            user,
            isAuthenticated: true,
          });
        } catch (error) {
          throw error;
        }
      },

      register: async (username: string, password: string) => {
        try {
          const user = await authApi.register({ username, password });
          // After registration, log the user in
          const tokenData = await authApi.login({ username, password });
          
          // Zustand persist middleware will automatically save to localStorage
          set({
            token: tokenData.access_token,
            user,
            isAuthenticated: true,
          });
        } catch (error) {
          throw error;
        }
      },

      logout: () => {
        // Zustand persist middleware will automatically clear localStorage
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
