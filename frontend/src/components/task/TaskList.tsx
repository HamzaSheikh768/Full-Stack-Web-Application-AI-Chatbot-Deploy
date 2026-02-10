'use client';

import { useState, useEffect, memo } from 'react';
import { TaskItem } from './TaskItem';
import { TaskFilters } from './TaskFilters';
import { SortControls } from '@/components/SortControls';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus } from 'lucide-react';
import { Task as ApiTask } from '@/lib/api';

interface TaskListProps {
  tasks: ApiTask[];
  loading?: boolean;
  onTaskUpdate: (task: ApiTask) => void;
  onTaskDelete: (taskId: string) => void;
  onTaskToggleComplete: (taskId: string, completed: boolean) => void;
  onAddTaskClick: () => void;
}

const TaskListComponent = ({ 
  tasks,
  loading = false,
  onTaskUpdate,
  onTaskDelete,
  onTaskToggleComplete,
  onAddTaskClick
}: TaskListProps) => {
  const [filteredTasks, setFilteredTasks] = useState<ApiTask[]>(tasks);
  const [filters, setFilters] = useState({
    status: 'all',
    priority: 'all',
    tags: [] as string[],
    dueDateFrom: '',
    dueDateTo: '',
    search: ''
  });
  const [sortBy, setSortBy] = useState('due_at'); // Default sort by due date
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Extract unique tags from tasks for the filter component
  const availableTags = Array.from(
    new Set(tasks.flatMap(task => task.tags || []))
  );

  // Subscribe to real-time updates from AI Chat
  useEffect(() => {
    const handleRealTimeTaskUpdate = (event: CustomEvent) => {
      const { updateType, taskData } = event.detail;

      switch(updateType) {
        case 'created':
          // Add new task to the list
          setFilteredTasks(prev => [...prev, taskData]);
          break;
        case 'updated':
          // Update existing task in the list
          setFilteredTasks(prev =>
            prev.map(task =>
              task.id === taskData.id ? { ...task, ...taskData } : task
            )
          );
          break;
        case 'completed':
          // Update task completion status
          setFilteredTasks(prev =>
            prev.map(task =>
              task.id === taskData.id ? { ...task, completed: true } : task
            )
          );
          break;
        case 'deleted':
          // Remove task from the list
          setFilteredTasks(prev =>
            prev.filter(task => task.id !== taskData.id)
          );
          break;
      }
    };

    // Listen for real-time updates from AI Chat
    window.addEventListener('taskUpdate', handleRealTimeTaskUpdate as EventListener);

    return () => {
      window.removeEventListener('taskUpdate', handleRealTimeTaskUpdate as EventListener);
    };
  }, []);

  // Apply filters and sorting when tasks, filters, or sort options change
  useEffect(() => {
    let result = [...tasks];

    // Apply status filter
    if (filters.status !== 'all') {
      result = result.filter(task =>
        filters.status === 'completed' ? task.status === 'completed' : task.status !== 'completed'
      );
    }

    // Apply priority filter
    if (filters.priority !== 'all') {
      result = result.filter(task => task.priority?.toLowerCase() === filters.priority.toLowerCase());
    }

    // Apply tags filter
    if (filters.tags.length > 0) {
      result = result.filter(task => 
        task.tags && filters.tags.some(tag => task.tags?.includes(tag))
      );
    }

    // Apply due date from filter
    if (filters.dueDateFrom) {
      const fromDate = new Date(filters.dueDateFrom);
      result = result.filter(task => 
        task.due_date && new Date(task.due_date) >= fromDate
      );
    }

    // Apply due date to filter
    if (filters.dueDateTo) {
      const toDate = new Date(filters.dueDateTo);
      result = result.filter(task => 
        task.due_date && new Date(task.due_date) <= toDate
      );
    }

    // Apply search filter
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchTerm) ||
        (task.description && task.description.toLowerCase().includes(searchTerm)) ||
        (task.tags && task.tags.some(tag => tag.toLowerCase().includes(searchTerm)))
      );
    }

    // Apply sorting
    result.sort((a, b) => {
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

    setFilteredTasks(result);
  }, [tasks, filters, sortBy, sortOrder]);

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, index) => (
          <Skeleton key={index} className="h-16 w-full" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-800 dark:text-white">Your Tasks</h2>
        <Button onClick={onAddTaskClick} className="w-full sm:w-auto">
          <Plus className="mr-2 h-4 w-4" /> Add Task
        </Button>
      </div>

      <TaskFilters 
        filters={filters} 
        onFilterChange={handleFilterChange} 
        availableTags={availableTags}
      />

      <SortControls 
        sortBy={sortBy} 
        sortOrder={sortOrder} 
        onSortChange={(newSortBy, newSortOrder) => {
          setSortBy(newSortBy);
          setSortOrder(newSortOrder);
        }} 
      />

      <div className="space-y-4">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">
              {tasks.length === 0
                ? "No tasks yet. Add your first task!"
                : "No tasks match your current filters."}
            </p>
          </div>
        ) : (
          filteredTasks.map(task => (
            <MemoizedTaskItem
              key={task.id}
              task={task}
              onUpdate={onTaskUpdate}
              onDelete={onTaskDelete}
              onToggleComplete={onTaskToggleComplete}
            />
          ))
        )}
      </div>
    </div>
  );
};

const MemoizedTaskItem = memo(TaskItem);

export { TaskListComponent as TaskList };