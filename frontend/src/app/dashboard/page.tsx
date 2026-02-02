'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { dashboardApi } from '@/lib/api';
import { taskApi } from '@/lib/api';
import { Task as ApiTask } from '@/lib/api';
import { TaskService } from '@/lib/task-service';
import { useAuth } from '@/contexts/AuthContext';

interface DashboardData {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  task_types: Record<string, number>;
  task_priorities: Record<string, number>;
}

interface DashboardStats {
  success: boolean;
  data: DashboardData;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardData | null>(null);
  const [tasks, setTasks] = useState<ApiTask[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [tasksLoading, setTasksLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [filterPriority, setFilterPriority] = useState<string>('');
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  // Define consistent colors for charts
  const CHART_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  // Handler for editing a task
  const handleEditTask = (task: ApiTask) => {
    // In a real application, this would navigate to an edit task page or open a modal
    console.log('Editing task:', task.id);
    toast.info('Edit functionality would open task editor in a real application');
  };

  // Handler for deleting a task
  const handleDeleteTask = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await TaskService.delete(taskId);
        toast.success('Task deleted successfully');
        // Refresh tasks after deletion
        await fetchTasks();
        // Also refresh stats since we removed a task
        await fetchDashboardStats();
      } catch (error) {
        console.error('Error deleting task:', error);
        toast.error('Failed to delete task');
      }
    }
  };

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchDashboardStats();
      fetchTasks();
    }
  }, [isAuthenticated]);

  // Effect to fetch tasks when filters change
  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [searchQuery, filterStatus, filterPriority, isAuthenticated]);

  const fetchDashboardStats = async () => {
    try {
      // Calculate dashboard stats from user's tasks instead of calling a dedicated endpoint
      const userTasks = await TaskService.getAll();

      // Calculate statistics from tasks
      const totalTasks = userTasks.length;
      const completedTasks = userTasks.filter(task => task.is_completed).length;
      const pendingTasks = totalTasks - completedTasks;

      // Count task types (recurrence patterns)
      const taskTypes: Record<string, number> = { none: 0, daily: 0, weekly: 0, monthly: 0, yearly: 0 };
      userTasks.forEach(task => {
        const type = task.recurrence_pattern || 'none';
        if (taskTypes.hasOwnProperty(type)) {
          taskTypes[type]++;
        } else {
          taskTypes['none']++;
        }
      });

      // Count task priorities
      const taskPriorities: Record<string, number> = { low: 0, medium: 0, high: 0 };
      userTasks.forEach(task => {
        const priority = task.priority || 'medium';
        if (taskPriorities.hasOwnProperty(priority)) {
          taskPriorities[priority]++;
        } else {
          taskPriorities['medium']++;
        }
      });

      const statsData = {
        total_tasks: totalTasks,
        completed_tasks: completedTasks,
        pending_tasks: pendingTasks,
        task_types: taskTypes,
        task_priorities: taskPriorities
      };

      setStats(statsData);
    } catch (error) {
      console.error('Error calculating dashboard stats:', error);
      toast.error('Failed to load dashboard statistics');
      // Set empty stats to avoid showing error state but with real field names
      setStats({
        total_tasks: 0,
        completed_tasks: 0,
        pending_tasks: 0,
        task_types: { none: 0, daily: 0, weekly: 0, monthly: 0, yearly: 0 },
        task_priorities: { low: 0, medium: 0, high: 0 }
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchTasks = async () => {
    try {
      setTasksLoading(true);

      // Fetch tasks using TaskService which handles field mapping
      let allTasks = await TaskService.getAll();

      // Apply client-side filtering since the API parameters may not work as expected
      if (searchQuery) {
        const term = searchQuery.toLowerCase();
        allTasks = allTasks.filter(task =>
          task.title.toLowerCase().includes(term) ||
          (task.description && task.description.toLowerCase().includes(term)) ||
          task.priority.toLowerCase().includes(term) ||
          task.type.toLowerCase().includes(term) ||
          (task.due_date && task.due_date.toLowerCase().includes(term))
        );
      }

      if (filterStatus) {
        if (filterStatus === 'completed') {
          allTasks = allTasks.filter(task => task.status === 'completed');
        } else if (filterStatus === 'pending') {
          allTasks = allTasks.filter(task => task.status === 'pending');
        }
      }

      if (filterPriority) {
        allTasks = allTasks.filter(task => task.priority === filterPriority);
      }

      setTasks(allTasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      toast.error('Failed to load tasks');
      setTasks([]);
    } finally {
      setTasksLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background py-4 sm:py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
          <div className="animate-pulse space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[1, 2, 3, 4].map((item) => (
                <div key={item} className="bg-card h-24 rounded-xl"></div>
              ))}
            </div>
            <div className="bg-card rounded-xl p-6">
              <div className="bg-muted h-64 rounded-lg"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="min-h-screen bg-background py-4 sm:py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
          <Card className="bg-card">
            <CardHeader>
              <CardTitle>Error Loading Dashboard</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Unable to load dashboard statistics. Please try again later.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Prepare data for charts
  const typeChartData = Object.entries(stats.task_types).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  const priorityChartData = Object.entries(stats.task_priorities).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  // Colors for charts
  const COLORS = CHART_COLORS;

  return (
    <div className="min-h-screen bg-background py-6 fade-in-up">
      <div className="container mx-auto px-4 md:px-6 lg:px-8 py-6 max-w-7xl">
        <div className="mb-8 sm:mb-12 fade-in-up" style={{ animationDelay: '0.1s' }}>
          <h1 className="text-3xl sm:text-4xl font-bold text-foreground">Dashboard</h1>
          <p className="text-base sm:text-lg text-muted-foreground mt-2">Overview of your task statistics and productivity metrics</p>
        </div>

        {/* Stats Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8 sm:mb-12">
          {/* Total Tasks Card */}
          <Card className="bg-card border border-border rounded-xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up" style={{ animationDelay: '0.2s' }}>
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="text-sm font-medium text-muted-foreground">Total Tasks</CardTitle>
                <p className="text-2xl sm:text-3xl font-bold mt-2 text-foreground">{stats.total_tasks}</p>
              </div>
              <div className="p-3 rounded-full bg-blue-100 dark:bg-blue-900/50">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">All tasks created</p>
            </CardContent>
          </Card>

          {/* Completed Tasks Card */}
          <Card className="bg-card border border-border rounded-xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up" style={{ animationDelay: '0.3s' }}>
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="text-sm font-medium text-muted-foreground">Completed</CardTitle>
                <p className="text-2xl sm:text-3xl font-bold mt-2 text-green-600 dark:text-green-400">{stats.completed_tasks}</p>
              </div>
              <div className="p-3 rounded-full bg-green-100 dark:bg-green-900/50">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600 dark:text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">Tasks completed</p>
            </CardContent>
          </Card>

          {/* Pending Tasks Card */}
          <Card className="bg-card border border-border rounded-xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up" style={{ animationDelay: '0.4s' }}>
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="text-sm font-medium text-muted-foreground">Pending</CardTitle>
                <p className="text-2xl sm:text-3xl font-bold mt-2 text-yellow-600 dark:text-yellow-400">{stats.pending_tasks}</p>
              </div>
              <div className="p-3 rounded-full bg-yellow-100 dark:bg-yellow-900/50">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-600 dark:text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v4" />
                  <path d="M12 16h.01" />
                </svg>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">Tasks awaiting completion</p>
            </CardContent>
          </Card>

          {/* Completion Rate Card */}
          <Card className="bg-card border border-border rounded-xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up" style={{ animationDelay: '0.5s' }}>
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="text-sm font-medium text-muted-foreground">Completion Rate</CardTitle>
                <p className="text-2xl sm:text-3xl font-bold mt-2 text-purple-600 dark:text-purple-400">
                  {stats.total_tasks > 0 ? Math.round((stats.completed_tasks / stats.total_tasks) * 100) : 0}%
                </p>
              </div>
              <div className="p-3 rounded-full bg-purple-100 dark:bg-purple-900/50">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600 dark:text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">Overall completion percentage</p>
            </CardContent>
          </Card>
        </div>

        {/* Search & Filter Section */}
        <div className="mb-8 sm:mb-12 fade-in-up" style={{ animationDelay: '0.6s' }}>
          <Card className="bg-card border border-border rounded-xl p-6">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">Task Search & Filter</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col sm:flex-row gap-4">
                <input
                  type="text"
                  placeholder="Search tasks..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1 px-4 py-2 border border-border rounded-lg bg-background text-foreground focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-4 py-2 border border-border rounded-lg bg-background text-foreground focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                >
                  <option value="">All Status</option>
                  <option value="completed">Completed</option>
                  <option value="pending">Pending</option>
                </select>
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className="px-4 py-2 border border-border rounded-lg bg-background text-foreground focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                >
                  <option value="">All Priorities</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tasks List Panel */}
        <div className="mb-8 sm:mb-12 fade-in-up" style={{ animationDelay: '0.7s' }}>
          <Card className="bg-card border border-border rounded-xl p-6">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">Your Tasks</CardTitle>
            </CardHeader>
            <CardContent>
              {tasksLoading ? (
                <div className="space-y-4">
                  {[1, 2, 3].map((item) => (
                    <div key={item} className="flex items-center justify-between p-3 border border-border rounded-lg animate-pulse">
                      <div className="flex items-center">
                        <div className="h-3 w-3 rounded-full bg-gray-300 dark:bg-gray-600 mr-3"></div>
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-32"></div>
                      </div>
                      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
                    </div>
                  ))}
                </div>
              ) : tasks.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground fade-in-up">
                  {searchQuery || filterStatus || filterPriority
                    ? "No tasks match your current filters."
                    : "No tasks found. Create your first task on the Tasks page!"}
                </div>
              ) : (
                <div className="space-y-4">
                  {tasks.map((task, index) => (
                    <div
                      key={task.id}
                      className={`flex items-center justify-between p-3 border border-border rounded-lg transition-all duration-300 hover:shadow-md hover:scale-[1.02] ${
                        task.is_completed ? 'bg-green-50/30 dark:bg-green-900/20' : 'bg-background hover:bg-gray-50/50 dark:hover:bg-gray-800/50'
                      } fade-in-up`}
                      style={{ animationDelay: `${0.8 + index * 0.1}s` }}
                    >
                      <div className="flex items-center flex-grow">
                        <div className={`h-3 w-3 rounded-full mr-3 ${
                          task.is_completed
                            ? 'bg-green-500'
                            : task.priority === 'high'
                              ? 'bg-red-500'
                              : task.priority === 'medium'
                                ? 'bg-yellow-500'
                                : 'bg-blue-500'
                        }`}></div>
                        <span className={task.is_completed ? 'line-through text-muted-foreground' : ''}>
                          {task.title}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`text-sm ${
                          task.priority === 'high' ? 'text-red-600 dark:text-red-400' :
                          task.priority === 'medium' ? 'text-yellow-600 dark:text-yellow-400' :
                          'text-blue-600 dark:text-blue-400'
                        }`}>
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                        </span>
                        <button
                          onClick={() => handleEditTask(task)}
                          className="ml-2 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 p-1 rounded hover:bg-blue-100 dark:hover:bg-blue-900/30"
                          aria-label="Edit task"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                          </svg>
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="ml-1 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 p-1 rounded hover:bg-red-100 dark:hover:bg-red-900/30"
                          aria-label="Delete task"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M3 6h18" />
                            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          {/* Task Types Chart */}
          <Card className="bg-card border border-border rounded-xl p-6">
            <CardHeader>
              <CardTitle className="text-base sm:text-lg">Task Distribution by Type</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={typeChartData}>
                  <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.3} />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--background))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '0.5rem'
                    }}
                  />
                  <Bar dataKey="value" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Task Distribution Visualization - Donut Chart */}
          <Card className="bg-card border border-border rounded-2xl p-6 hover:shadow-lg transition-all duration-300 fade-in-up" style={{ animationDelay: '0.8s' }}>
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-foreground">Task Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={priorityChartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}  /* Creating donut shape */
                    outerRadius={80}
                    paddingAngle={2}
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${percent ? (percent * 100).toFixed(0) : '0'}%`}
                  >
                    {priorityChartData.map((entry, index) => {
                      // Map colors according to specification: High (red-blue mix), Medium (blue), Low (gray)
                      let color;
                      if (entry.name.toLowerCase() === 'high') {
                        color = '#ef4444'; // red
                      } else if (entry.name.toLowerCase() === 'medium') {
                        color = '#3b82f6'; // blue
                      } else if (entry.name.toLowerCase() === 'low') {
                        color = '#6b7280'; // gray
                      } else {
                        // Fallback colors for other types
                        const fallbackColors = ['#ef4444', '#3b82f6', '#6b7280']; // red, blue, gray
                        color = fallbackColors[index % fallbackColors.length];
                      }

                      return <Cell key={`cell-${index}`} fill={color} />;
                    })}
                  </Pie>
                  <Tooltip
                    formatter={(value, name, props) => [`${value} tasks`, name]}
                    contentStyle={{
                      backgroundColor: 'hsl(var(--background))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '0.5rem',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}