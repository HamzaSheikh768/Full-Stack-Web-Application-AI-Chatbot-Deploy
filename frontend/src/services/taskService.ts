import { Task } from '@/lib/api';

/**
 * Service for handling task operations including filtering and sorting
 */
export class TaskService {
  /**
   * Filter tasks based on provided criteria
   */
  static filterTasks(
    tasks: Task[],
    filters: {
      status?: string;
      priority?: string;
      tags?: string[];
      dueDateFrom?: string;
      dueDateTo?: string;
      search?: string;
    }
  ): Task[] {
    return tasks.filter(task => {
      // Apply status filter
      if (filters.status && filters.status !== 'all') {
        if (filters.status === 'completed' && task.status !== 'completed') return false;
        if (filters.status === 'pending' && task.status === 'completed') return false;
      }

      // Apply priority filter
      if (filters.priority && filters.priority !== 'all') {
        if (task.priority?.toLowerCase() !== filters.priority.toLowerCase()) return false;
      }

      // Apply tags filter
      if (filters.tags && filters.tags.length > 0) {
        if (!task.tags || !filters.tags.some(tag => task.tags?.includes(tag))) return false;
      }

      // Apply due date from filter
      if (filters.dueDateFrom) {
        const fromDate = new Date(filters.dueDateFrom);
        if (!task.due_date || new Date(task.due_date) < fromDate) return false;
      }

      // Apply due date to filter
      if (filters.dueDateTo) {
        const toDate = new Date(filters.dueDateTo);
        if (!task.due_date || new Date(task.due_date) > toDate) return false;
      }

      // Apply search filter
      if (filters.search) {
        const searchTerm = filters.search.toLowerCase();
        const matchesTitle = task.title.toLowerCase().includes(searchTerm);
        const matchesDescription = task.description?.toLowerCase().includes(searchTerm);
        const matchesTags = task.tags?.some(tag => tag.toLowerCase().includes(searchTerm));

        if (!matchesTitle && !matchesDescription && !matchesTags) return false;
      }

      return true;
    });
  }

  /**
   * Sort tasks based on provided criteria
   */
  static sortTasks(
    tasks: Task[],
    sortBy: string = 'due_at',
    sortOrder: 'asc' | 'desc' = 'asc'
  ): Task[] {
    return [...tasks].sort((a, b) => {
      let aValue: any, bValue: any;

      switch (sortBy) {
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        case 'priority':
          // Define priority order: high > medium > low
          const priorityOrder = { 'high': 3, 'medium': 2, 'low': 1 };
          aValue = priorityOrder[a.priority as keyof typeof priorityOrder] || 0;
          bValue = priorityOrder[b.priority as keyof typeof priorityOrder] || 0;
          break;
        case 'due_at':
          aValue = a.due_date ? new Date(a.due_date).getTime() : Infinity; // Unset due dates go last
          bValue = b.due_date ? new Date(b.due_date).getTime() : Infinity;
          break;
        case 'created_at':
        default:
          aValue = new Date(a.created_at).getTime();
          bValue = new Date(b.created_at).getTime();
          break;
      }

      if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });
  }

  /**
   * Apply both filtering and sorting to tasks
   */
  static filterAndSortTasks(
    tasks: Task[],
    filters: {
      status?: string;
      priority?: string;
      tags?: string[];
      dueDateFrom?: string;
      dueDateTo?: string;
      search?: string;
    },
    sortBy: string = 'due_at',
    sortOrder: 'asc' | 'desc' = 'asc'
  ): Task[] {
    const filteredTasks = this.filterTasks(tasks, filters);
    return this.sortTasks(filteredTasks, sortBy, sortOrder);
  }
}