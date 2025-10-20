// API Response Types based on backend Pydantic schemas

export interface User {
  id: number;
  username: string;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
  plans?: Plan[]; // Optional, might not always be included
}

export interface Plan {
  id: number;
  title: string;
  is_done: boolean;
  note_id: number;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// API Request Types

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface NoteCreateRequest {
  title: string;
  content: string;
}

export interface NoteUpdateRequest {
  title?: string;
  content?: string;
}

export interface PlanCreateRequest {
  title: string;
  is_done: boolean;
}

export interface PlanUpdateRequest {
  title?: string;
  is_done?: boolean;
}

// UI State Types

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  initialize: () => Promise<void>;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export interface ApiError {
  detail: string;
}
