
import { getCurrentUserId } from './jwt-utils';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generic API request function with authentication
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  includeAuth: boolean = true
): Promise<T> {
  let headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Add authorization header if needed and available
  if (includeAuth) {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const mergedHeaders: Record<string, string> = { ...headers };
  if (options.headers) {
    Object.assign(mergedHeaders, options.headers);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: mergedHeaders,
    // Prevent caching to ensure fresh data on page refresh
    cache: 'no-store',
  });

  if (!response.ok) {
    // Check if the response is JSON before trying to parse it
    const contentType = response.headers.get('content-type');
    let errorData = {};

    if (contentType && contentType.includes('application/json')) {
      errorData = await response.json().catch(() => ({}));
    } else {
      // If it's not JSON, try to get the text content for debugging
      const errorText = await response.text().catch(() => '');
      console.error('Non-JSON response received:', errorText.substring(0, 200) + '...');
      throw new Error(`HTTP error! status: ${response.status}. Received non-JSON response.`);
    }

    throw new Error((errorData as any).detail || `HTTP error! status: ${response.status}`);
  }

  // Handle responses without body (e.g., 204 No Content)
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * Task API functions
 */
export const taskApi = {
  /**
   * Get all tasks for the authenticated user
   */
  getTasks: async (params?: {
    completed?: boolean;
    priority?: string;
    due_date?: string;
    search?: string;
    sort?: string;
    order?: 'asc' | 'desc';
    limit?: number;
    offset?: number;
  }) => {
    const queryParams = new URLSearchParams();

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          // Map frontend parameter names to backend parameter names
          let paramName = key;
          if (key === 'completed') {
            paramName = 'status_filter';
            // Convert boolean to string for backend
            value = value ? 'completed' : 'pending';
          }

          queryParams.append(paramName, String(value));
        }
      });
    }

    const queryString = queryParams.toString();

    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    const endpoint = `/api/${userId}/tasks${queryString ? `?${queryString}` : ''}`;

    const response = await apiRequest<TaskListResponse>(endpoint, {}, true);
    // Extract tasks from the response.data.tasks structure
    const tasks = response.data?.tasks || [];

    // Add computed fields for compatibility with existing components
    return tasks.map(task => ({
      ...task,
      status: task.is_completed ? 'completed' : 'pending',
      type: task.recurrence_pattern
    }));
  },

  /**
   * Create a new task
   */
  createTask: async (taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await apiRequest<{ success: boolean; data: Task }>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    }, true);
    return response.data; // Extract task directly from response.data
  },

  /**
   * Get a specific task
   */
  getTask: async (taskId: string) => {
    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await apiRequest<{ success: boolean; data: Task }>(`/api/${userId}/tasks/${taskId}`, {}, true);
    const task = response.data; // Extract task directly from response.data

    // Add computed fields for compatibility with existing components
    return {
      ...task,
      status: task.is_completed ? 'completed' : 'pending',
      type: task.recurrence_pattern
    };
  },

  /**
   * Update a task
   */
  updateTask: async (taskId: string, taskData: Partial<Task>) => {
    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await apiRequest<{ success: boolean; data: Task }>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }, true);
    const task = response.data; // Extract task directly from response.data

    // Add computed fields for compatibility with existing components
    return {
      ...task,
      status: task.is_completed ? 'completed' : 'pending',
      type: task.recurrence_pattern
    };
  },

  /**
   * Delete a task
   */
  deleteTask: async (taskId: string) => {
    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    return apiRequest<{ success: boolean; message: string }>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    }, true);
  },

  /**
   * Update task completion status
   */
  updateTaskCompletion: async (taskId: string, isCompleted: boolean) => {
    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await apiRequest<{ success: boolean; data: Task }>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ is_completed: isCompleted }), // Send the completion status in the request body
    }, true);
    const task = response.data; // Extract task directly from response.data

    // Add computed fields for compatibility with existing components
    return {
      ...task,
      status: task.is_completed ? 'completed' : 'pending',
      type: task.recurrence_pattern
    };
  },
};

export const dashboardApi = {
  /**
   * Get dashboard statistics
   */
  getStats: async () => {
    // Public access only - no authentication required
    return apiRequest<DashboardStatsResponse>('/api/dashboard/stats', {}, false);
  },
};

export const chatApi = {
  /**
   * Send a message to the AI assistant
   */
  sendMessage: async (message: string, conversationId?: number) => {
    // Get user ID ensuring consistency between localStorage and token
    const tokenUserId = getCurrentUserId();
    const storageUserId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

    // Prefer the user ID from the token to ensure it matches the authenticated user
    // but fall back to storage if token decoding fails
    const userId = tokenUserId || storageUserId;

    if (!userId) {
      throw new Error('User not authenticated');
    }

    // Get the token for authentication
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    if (!token) {
      throw new Error('Authentication token not found');
    }

    // Use direct API call to the backend API with authentication
    const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,  // Add JWT token for authentication
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      })
    });

    if (!response.ok) {
      // Check if the response is JSON before trying to parse it
      const contentType = response.headers.get('content-type');
      let errorData = {};

      if (contentType && contentType.includes('application/json')) {
        errorData = await response.json().catch(() => ({}));
      } else {
        // If it's not JSON, try to get the text content for debugging
        const errorText = await response.text().catch(() => '');
        console.error('Non-JSON response received in chat API:', errorText.substring(0, 200) + '...');
        throw new Error(`HTTP error! status: ${response.status}. Received non-JSON response in chat API.`);
      }

      throw new Error((errorData as any).detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  },
};

// Define TypeScript interfaces for our API models
export interface Task {
  id: string;  // Changed from number to string to match backend UUID
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean; // Matches backend Task model (completed field)
  priority: 'low' | 'medium' | 'high';
  recurrence_pattern: 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly'; // Matches backend Task model
  due_date?: string; // ISO string format
  created_at: string; // ISO string format
  updated_at: string; // ISO string format
  order_index?: string;
  // Advanced features
  tags?: string[]; // Array of tags
  remind_at?: string; // Reminder time
  is_recurring?: boolean; // Whether task is recurring
  recurrence_pattern_details?: any; // Detailed recurrence pattern
  next_due_date?: string; // Next due date for recurring tasks
  // Computed fields for compatibility with existing components
  status?: string; // Computed from is_completed (completed/pending)
  type?: string; // Computed from recurrence_pattern
}

export interface TaskListResponse {
  success: boolean;
  data: {
    tasks: Task[];
    total: number;
  };
  message?: string;
}

export interface DashboardStatsResponse {
  success: boolean;
  data: {
    total_tasks: number;
    completed_tasks: number;
    pending_tasks: number;
    task_types: Record<string, number>;
    task_priorities: Record<string, number>;
  };
}