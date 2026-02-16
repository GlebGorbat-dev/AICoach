import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  token: string;
}

export interface Chat {
  id: string;
  title: string;
  datetimeInserted?: string;  // May come from backend
  datetimeCreated?: string;   // Alternative name
  datetimeUpdated: string;
}

export interface Message {
  id: string;
  content: string;
  author: 'user' | 'ai';
  datetimeCreated: string;
}

export interface PromptTextRequest {
  text: string;
  promptTemplate?: string;
}

export interface AgentResponse {
  text: string | null;
}

export interface AmountOfDocumentsResponse {
  amountOfDocuments: number;
}

// API Methods
export const authAPI = {
  register: async (data: RegisterRequest): Promise<TokenResponse> => {
    const response = await api.post('/api/user/register', data);
    return response.data.data;
  },

  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await api.post('/api/user/login', data);
    return response.data.data;
  },
};

export const chatAPI = {
  getAll: async (pageSize = 10, pageIndex = 0): Promise<{ paging: any; data: Chat[] }> => {
    const response = await api.get(`/api/chat/all?pageSize=${pageSize}&pageIndex=${pageIndex}`);
    return response.data.data;
  },

  get: async (chatId: string): Promise<Chat> => {
    const response = await api.get(`/api/chat/${chatId}`);
    return response.data.data;
  },

  create: async (): Promise<Chat> => {
    const response = await api.post('/api/chat');
    return response.data.data;
  },

  delete: async (chatId: string): Promise<void> => {
    await api.delete(`/api/chat/${chatId}`);
  },

  updateTitle: async (chatId: string, title: string): Promise<Chat> => {
    const response = await api.patch(`/api/chat/${chatId}/title`, { title });
    return response.data.data;
  },
};

export const agentAPI = {
  sendMessage: async (chatId: string, data: PromptTextRequest): Promise<AgentResponse> => {
    const response = await api.post(`/api/agent/${chatId}`, data);
    return response.data.data;
  },

  getMessages: async (chatId: string, pageSize = 10, pageIndex = 0): Promise<{ paging: any; data: Message[] }> => {
    const response = await api.get(`/api/agent/${chatId}/all?pageSize=${pageSize}&pageIndex=${pageIndex}`);
    return response.data.data;
  },

  getDocumentsCount: async (): Promise<AmountOfDocumentsResponse> => {
    const response = await api.get('/api/agent/documents');
    return response.data.data;
  },
};

export default api;

