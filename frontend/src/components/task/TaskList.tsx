'use client';

import { useState, useEffect } from 'react';
import { TaskItem } from './TaskItem';
import { TaskFilters } from './TaskFilters';
import { Button } from '../ui/button';
import { Skeleton } from '../ui/skeleton';
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

export function TaskList({
  tasks,
  loading = false,
  onTaskUpdate,
  onTaskDelete,
  onTaskToggleComplete,
  onAddTaskClick
}: TaskListProps) {
  const [filteredTasks, setFilteredTasks] = useState<ApiTask[]>(tasks);
  const [filters, setFilters] = useState({
    status: undefined as 'completed' | 'pending' | undefined,
    priority: '',
    dueDate: '',
    search: ''
  });

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

  // Apply filters when tasks or filters change
  useEffect(() => {
    let result = [...tasks];

    // Apply status filter
    if (filters.status !== undefined) {
      result = result.filter(task =>
        filters.status === 'completed' ? task.status === 'completed' : task.status !== 'completed'
      );
    }

    // Apply priority filter
    if (filters.priority) {
      result = result.filter(task => task.priority?.toLowerCase() === filters.priority.toLowerCase());
    }

    // Apply search filter
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchTerm) ||
        (task.description && task.description.toLowerCase().includes(searchTerm))
      );
    }

    setFilteredTasks(result);
  }, [tasks, filters]);

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

      <TaskFilters filters={filters} onFilterChange={handleFilterChange} />

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
            <TaskItem
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
}