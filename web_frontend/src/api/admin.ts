import { api } from './client'
import type { User, Note } from '../types'

export const adminApi = {
  async getAllUsers(): Promise<User[]> {
    const response = await api.get<User[]>('/admin/users')
    return response.data
  },

  async getAllNotes(): Promise<Note[]> {
    const response = await api.get<Note[]>('/admin/notes')
    return response.data
  },

  async getUserNotes(userId: number): Promise<Note[]> {
    const response = await api.get<Note[]>(`/admin/users/${userId}/notes`)
    return response.data
  },
}
