import { api, handleApiError } from './client';
import type {
  Note,
  NoteCreateRequest,
  NoteUpdateRequest,
} from '../types';

export const notesApi = {
  // Get all notes for current user
  getAll: async (): Promise<Note[]> => {
    try {
      const response = await api.get<Note[]>('/notes');
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Create a new note
  create: async (data: NoteCreateRequest): Promise<Note> => {
    try {
      const response = await api.post<Note>('/notes', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Update a note
  update: async (id: number, data: NoteUpdateRequest): Promise<Note> => {
    try {
      const response = await api.put<Note>(`/notes/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Delete a note
  delete: async (id: number): Promise<void> => {
    try {
      await api.delete(`/notes/${id}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
