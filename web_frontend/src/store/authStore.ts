import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '../api/auth';
import type { User, AuthState } from '../types';

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (username: string, password: string) => {
        try {
          const tokenData = await authApi.login({ username, password });
          
          // Store token
          localStorage.setItem('token', tokenData.access_token);
          
          // Create user object (backend doesn't return user on login)
          const user: User = {
            id: 0, // Will be populated when needed
            username,
          };
          
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
          
          localStorage.setItem('token', tokenData.access_token);
          
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
        localStorage.removeItem('token');
        localStorage.removeItem('user');
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
