import { api } from './client'
import type { User } from '../types'

export const usersApi = {
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me')
    return response.data
  },
}
