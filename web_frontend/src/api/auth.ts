import { api, handleApiError } from './client';
import type {
  LoginRequest,
  RegisterRequest,
  Token,
  User,
} from '../types';

export const authApi = {
  // Login with form-data (OAuth2 requirement)
  login: async (credentials: LoginRequest): Promise<Token> => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);

      const response = await api.post<Token>('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Register with JSON
  register: async (credentials: RegisterRequest): Promise<User> => {
    try {
      const response = await api.post<User>('/auth/register', credentials);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
