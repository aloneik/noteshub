import { api, handleApiError } from './client';
import type {
  Plan,
  PlanCreateRequest,
  PlanUpdateRequest,
} from '../types';

export const plansApi = {
  // Get all plans for a note
  getAll: async (noteId: number): Promise<Plan[]> => {
    try {
      const response = await api.get<Plan[]>(`/notes/${noteId}/plans`);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Create a new plan
  create: async (noteId: number, data: PlanCreateRequest): Promise<Plan> => {
    try {
      const response = await api.post<Plan>(`/notes/${noteId}/plans`, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Update a plan
  update: async (
    noteId: number,
    planId: number,
    data: PlanUpdateRequest
  ): Promise<Plan> => {
    try {
      const response = await api.put<Plan>(
        `/notes/${noteId}/plans/${planId}`,
        data
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Delete a plan
  delete: async (noteId: number, planId: number): Promise<void> => {
    try {
      await api.delete(`/notes/${noteId}/plans/${planId}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
