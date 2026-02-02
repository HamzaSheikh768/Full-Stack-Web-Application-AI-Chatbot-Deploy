'use client';

import React, { useState, useEffect } from 'react';
import { TaskForm, TaskFormData } from '@/components/tasks/TaskForm';
import { SearchableTaskList } from '@/components/tasks/SearchableTaskList';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

// Import the Task type from the API
import { TaskService } from '@/lib/task-service';
import { Task } from '@/lib/api'; // Use the Task type from the API which handles mapping

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isCreating, setIsCreating] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loadingIds, setLoadingIds] = useState<string[]>([]); // Track IDs of tasks being processed
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Fetch tasks on component mount (only if authenticated)
  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await TaskService.getAll();
      setTasks(tasksData);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      toast.error('Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (formData: TaskFormData) => {
    try {
      setIsCreating(true);
      const newTask = await TaskService.create({
        ...formData,
        // The type is already in the correct format (lowercase) from the form
        type: formData.type || 'daily'
      });

      // Refresh the task list from the backend to ensure consistency
      await fetchTasks();
      toast.success('Task created successfully!');

      // Reset form state
      setEditingTask(null);
    } catch (error) {
      console.error('Error creating task:', error);
      toast.error('Failed to create task');
    } finally {
      setIsCreating(false);
    }
  };

  const handleUpdateTask = async (formData: TaskFormData) => {
    if (!editingTask) return;

    try {
      setIsCreating(true);
      // In a public access model, we're using a mock user ID
      const updatedTask = await TaskService.update(
        editingTask.id,
        {
          title: formData.title,
          description: formData.description,
          priority: formData.priority.toLowerCase() as 'low' | 'medium' | 'high',
          type: (formData.type as 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly') || editingTask.type || 'daily', // Use provided type or fallback to existing type
          due_date: formData.dueDate,
        }
      );

      // Refresh the task list from the backend to ensure consistency
      await fetchTasks();
      toast.success('Task updated successfully!');

      // Reset form state
      setEditingTask(null);
    } catch (error) {
      console.error('Error updating task:', error);
      toast.error('Failed to update task');
    } finally {
      setIsCreating(false);
    }
  };

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      // Add to loading IDs
      setLoadingIds(prev => [...prev, id]);

      await TaskService.toggleCompletion(id, completed);

      // Refresh the task list from the backend to ensure consistency
      await fetchTasks();

      toast.success(`Task ${completed ? 'completed' : 'marked as incomplete'}!`);
    } catch (error) {
      console.error('Error updating task completion:', error);
      toast.error('Failed to update task status');
    } finally {
      // Remove from loading IDs
      setLoadingIds(prev => prev.filter(loadingId => loadingId !== id));

      // Add animation effect for task completion
      if (completed) {
        const taskElement = document.getElementById(`task-${id}`);
        if (taskElement) {
          taskElement.classList.add('scale-95', 'opacity-50');
          setTimeout(() => {
            taskElement.classList.remove('scale-95', 'opacity-50');
          }, 300);
        }
      }
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleDeleteTask = async (id: string) => {
    try {
      // Add to loading IDs
      setLoadingIds(prev => [...prev, id]);

      // Add animation effect for task deletion
      const taskElement = document.getElementById(`task-${id}`);
      if (taskElement) {
        taskElement.classList.add('opacity-0', 'translate-x-full');
        // Wait for animation to complete before deleting
        await new Promise(resolve => setTimeout(resolve, 300));
      }

      await TaskService.delete(id);

      // Refresh the task list from the backend to ensure consistency
      await fetchTasks();
      toast.success('Task deleted successfully!');
    } catch (error) {
      console.error('Error deleting task:', error);
      toast.error('Failed to delete task');
    } finally {
      // Remove from loading IDs
      setLoadingIds(prev => prev.filter(loadingId => loadingId !== id));
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background py-4 sm:py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
          <div className="animate-pulse space-y-6">
            <div className="bg-card h-24 rounded-xl"></div>
            <div className="bg-card h-64 rounded-xl"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background py-6 sm:py-8 fade-in-up">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
        {/* Animated heading with underline as per specification */}
        <div className="mb-8 sm:mb-10 relative">
          <h1 className="text-3xl sm:text-4xl font-bold text-foreground inline-block relative group">
            Tasks
            <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 dark:bg-blue-400 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></span>
          </h1>
        </div>

        <Card className="bg-card border border-border rounded-2xl hover:shadow-lg transition-all duration-300">
          <CardHeader className="border-b border-border pb-4 sm:pb-6">
            <CardTitle className="text-xl sm:text-2xl font-bold text-foreground">Task Management</CardTitle>
            <p className="text-sm sm:text-base text-muted-foreground">
              Create, manage, and track your tasks efficiently
            </p>
          </CardHeader>
          <CardContent className="pt-6 sm:pt-8">
            {/* Task Creation/Editing Form */}
            {(editingTask ? (
              <div className="mb-6 sm:mb-8">
                <h2 className="text-lg sm:text-xl font-semibold mb-4">Edit Task</h2>
                <TaskForm
                  key={`edit-${editingTask.id}`}
                  onSubmit={handleUpdateTask}
                  onCancel={handleCancelEdit}
                  initialData={{
                    title: editingTask.title,
                    description: editingTask.description || "",
                    priority: editingTask.priority,
                    type: (editingTask.type as 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly') || "daily",
                    dueDate: editingTask.due_date || ""
                  }}
                  isSubmitting={isCreating}
                />
              </div>
            ) : (
              <div className="mb-6 sm:mb-8 animate-slide-up">
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 gap-2">
                  <h2 className="text-lg sm:text-xl font-semibold">Create New Task</h2>
                </div>
                <TaskForm
                  key="create-task"
                  onSubmit={handleCreateTask}
                  isSubmitting={isCreating}
                />
              </div>
            ))}

            {/* Task List */}
            <div>
              <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 gap-2">
                <h2 className="text-lg sm:text-xl font-semibold">Your Tasks</h2>
                <p className="text-sm sm:text-base text-muted-foreground">
                  {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                </p>
              </div>

              <SearchableTaskList
                tasks={tasks}
                onToggleComplete={handleToggleComplete}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
                loadingIds={loadingIds}
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}