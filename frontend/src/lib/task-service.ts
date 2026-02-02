import { taskApi } from './api';

// Define the shape of our input for creating/updating tasks
interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high'; // Updated to match backend API
  type?: 'daily' | 'weekly' | 'monthly' | 'yearly' | 'none'; // For compatibility with form, maps to recurrence_pattern
  dueDate?: string; // Using string format for API compatibility
}

interface UpdateTaskInput {
  title?: string;
  description?: string;
  is_completed?: boolean; // Updated to match backend API (using is_completed instead of status)
  priority?: 'low' | 'medium' | 'high'; // Updated to match backend API
  type?: 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly'; // For compatibility with form, maps to recurrence_pattern
  due_date?: string; // Using string format for API compatibility
}

/**
 * Service for managing tasks with CRUD operations
 */
export class TaskService {
  /**
   * Get all tasks (authenticated access)
   */
  static async getAll() {
    try {
      const tasks = await taskApi.getTasks();
      return tasks;
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw new Error('Failed to fetch tasks');
    }
  }

  /**
   * Get a single task by ID (authenticated access)
   */
  static async getById(id: string) {
    try {
      const task = await taskApi.getTask(id);
      return task;
    } catch (error) {
      console.error('Error fetching task:', error);
      throw new Error('Failed to fetch task');
    }
  }

  /**
   * Create a new task (authenticated access)
   */
  static async create(input: CreateTaskInput) {
    try {
      // Convert our input to match the backend API format
      const taskData = {
        title: input.title,
        description: input.description || '',
        is_completed: false, // Default to false (not completed)
        priority: input.priority || 'medium', // Default to medium
        recurrence_pattern: (input.type ? input.type.toLowerCase() : 'none') as 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly', // Send as recurrence_pattern field that backend expects
        due_date: input.dueDate,
      };

      const newTask = await taskApi.createTask(taskData);
      return newTask;
    } catch (error) {
      console.error('Error creating task:', error);
      throw new Error('Failed to create task');
    }
  }

  /**
   * Update an existing task (authenticated access)
   */
  static async update(id: string, input: Partial<UpdateTaskInput>) {
    try {
      // Prepare update data, converting to match backend API format
      const updateData: any = {};
      if (input.title !== undefined) updateData.title = input.title;
      if (input.description !== undefined) updateData.description = input.description;
      if (input.is_completed !== undefined) updateData.is_completed = input.is_completed;
      if (input.priority !== undefined) updateData.priority = input.priority;
      if (input.type !== undefined) updateData.recurrence_pattern = input.type;
      if (input.due_date !== undefined) updateData.due_date = input.due_date;

      const updatedTask = await taskApi.updateTask(id, updateData);
      return updatedTask;
    } catch (error) {
      console.error('Error updating task:', error);
      throw new Error('Failed to update task');
    }
  }

  /**
   * Delete a task (authenticated access)
   */
  static async delete(id: string) {
    try {
      await taskApi.deleteTask(id);
      return true;
    } catch (error) {
      console.error('Error deleting task:', error);
      throw new Error('Failed to delete task');
    }
  }

  /**
   * Toggle task completion status (authenticated access)
   */
  static async toggleCompletion(id: string, completed: boolean) {
    try {
      // Pass the completion status to the API
      const updatedTask = await taskApi.updateTaskCompletion(id, completed);
      return updatedTask;
    } catch (error) {
      console.error('Error updating task completion:', error);
      throw new Error('Failed to update task completion status');
    }
  }
}