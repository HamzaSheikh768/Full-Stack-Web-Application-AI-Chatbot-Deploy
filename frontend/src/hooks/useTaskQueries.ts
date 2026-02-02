import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { taskApi } from '@/lib/api';
import { Task } from '@/lib/api';

// Query keys for React Query
const QUERY_KEYS = {
  tasks: () => ['tasks'],
  task: (taskId: string) => ['task', taskId],
};

// Custom hook to get all tasks
export function useTasks() {
  return useQuery({
    queryKey: QUERY_KEYS.tasks(),
    queryFn: () => taskApi.getTasks(),
    enabled: true, // Always enabled since no authentication is required
  });
}

// Custom hook to get a specific task
export function useTask(taskId: string) {
  return useQuery({
    queryKey: QUERY_KEYS.task(taskId),
    queryFn: () => taskApi.getTask(taskId),
    enabled: !!taskId,
  });
}

// Custom hook to create a new task
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>) =>
      taskApi.createTask(taskData),
    onMutate: async (taskData) => {
      // Cancel outgoing refetches (so they don't overwrite our optimistic update)
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.tasks() });

      // Optimistically add the new task to the list
      const optimisticTask: Task = {
        ...taskData,
        id: `optimistic-${Date.now()}`,
        user_id: '', // Will be filled by backend
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        status: 'pending',
      };

      // Snapshot the previous value
      const previousTasks = queryClient.getQueryData<Task[]>(QUERY_KEYS.tasks());

      // Optimistically update the cache
      queryClient.setQueryData<Task[]>(
        QUERY_KEYS.tasks(),
        (oldTasks = []) => [...oldTasks, optimisticTask]
      );

      return { previousTasks, optimisticTask };
    },
    onError: (err, newTask, context) => {
      // Rollback the optimistic update if there's an error
      if (context?.previousTasks) {
        queryClient.setQueryData(QUERY_KEYS.tasks(), context.previousTasks);
      }
    },
    onSuccess: (newTask, taskData, context) => {
      // Update the optimistic task with the actual server response
      queryClient.setQueryData<Task[]>(
        QUERY_KEYS.tasks(),
        (oldTasks = []) =>
          oldTasks.map(task =>
            task.id === context?.optimisticTask.id ? newTask : task
          )
      );

      // Store the actual task in the cache
      queryClient.setQueryData(QUERY_KEYS.task(newTask.id), newTask);
    },
  });
}

// Custom hook to update a task
export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ taskId, taskData }: { taskId: string; taskData: Partial<Task> }) =>
      taskApi.updateTask(taskId, taskData),
    onMutate: async ({ taskId, taskData }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.task(taskId) });
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.tasks() });

      // Snapshot the previous values
      const previousTask = queryClient.getQueryData<Task>(QUERY_KEYS.task(taskId));
      const previousTasks = queryClient.getQueryData<Task[]>(QUERY_KEYS.tasks());

      // Optimistically update the specific task
      if (previousTask) {
        const updatedTask = { ...previousTask, ...taskData, updated_at: new Date().toISOString() };
        queryClient.setQueryData(QUERY_KEYS.task(taskId), updatedTask);

        // Optimistically update the tasks list
        queryClient.setQueryData<Task[]>(
          QUERY_KEYS.tasks(),
          (oldTasks = []) =>
            oldTasks.map(task =>
              task.id === taskId ? updatedTask : task
            )
        );
      }

      return { previousTask, previousTasks };
    },
    onError: (err, { taskId, taskData }, context) => {
      // Rollback the optimistic update if there's an error
      if (context?.previousTask) {
        queryClient.setQueryData(QUERY_KEYS.task(taskId), context.previousTask);
      }
      if (context?.previousTasks) {
        queryClient.setQueryData(QUERY_KEYS.tasks(), context.previousTasks);
      }
    },
    onSuccess: (updatedTask, { taskId, taskData }, context) => {
      // The optimistic update was already applied, so we just ensure the cache is updated with the server response
      queryClient.setQueryData(QUERY_KEYS.task(taskId), updatedTask);

      // Update the tasks list with the server response
      queryClient.setQueryData<Task[]>(
        QUERY_KEYS.tasks(),
        (oldTasks = []) =>
          oldTasks.map(task =>
            task.id === taskId ? updatedTask : task
          )
      );
    },
  });
}

// Custom hook to update task completion
export function useUpdateTaskCompletion() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ taskId, completed }: { taskId: string; completed: boolean }) =>
      taskApi.updateTaskCompletion(taskId, completed),
    onMutate: async ({ taskId, completed }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.task(taskId) });
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.tasks() });

      // Snapshot the previous values
      const previousTask = queryClient.getQueryData<Task>(QUERY_KEYS.task(taskId));
      const previousTasks = queryClient.getQueryData<Task[]>(QUERY_KEYS.tasks());

      // Optimistically update the specific task
      if (previousTask) {
        const updatedTask = { ...previousTask, completed, updated_at: new Date().toISOString() };
        queryClient.setQueryData(QUERY_KEYS.task(taskId), updatedTask);

        // Optimistically update the tasks list
        queryClient.setQueryData<Task[]>(
          QUERY_KEYS.tasks(),
          (oldTasks = []) =>
            oldTasks.map(task =>
              task.id === taskId ? updatedTask : task
            )
        );
      }

      return { previousTask, previousTasks };
    },
    onError: (err, { taskId, completed }, context) => {
      // Rollback the optimistic update if there's an error
      if (context?.previousTask) {
        queryClient.setQueryData(QUERY_KEYS.task(taskId), context.previousTask);
      }
      if (context?.previousTasks) {
        queryClient.setQueryData(QUERY_KEYS.tasks(), context.previousTasks);
      }
    },
    onSuccess: (updatedTask, { taskId, completed }, context) => {
      // The optimistic update was already applied, so we just ensure the cache is updated with the server response
      queryClient.setQueryData(QUERY_KEYS.task(taskId), updatedTask);

      // Update the tasks list with the server response
      queryClient.setQueryData<Task[]>(
        QUERY_KEYS.tasks(),
        (oldTasks = []) =>
          oldTasks.map(task =>
            task.id === taskId ? updatedTask : task
          )
      );
    },
  });
}

// Custom hook to delete a task
export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (taskId: string) => taskApi.deleteTask(taskId),
    onMutate: async (taskId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.task(taskId) });
      await queryClient.cancelQueries({ queryKey: QUERY_KEYS.tasks() });

      // Snapshot the previous values
      const previousTask = queryClient.getQueryData<Task>(QUERY_KEYS.task(taskId));
      const previousTasks = queryClient.getQueryData<Task[]>(QUERY_KEYS.tasks());

      // Optimistically remove the task from the list
      queryClient.setQueryData<Task[]>(
        QUERY_KEYS.tasks(),
        (oldTasks = []) => oldTasks.filter(task => task.id !== taskId)
      );

      // Remove the specific task from the cache
      queryClient.removeQueries({
        queryKey: QUERY_KEYS.task(taskId),
      });

      return { previousTask, previousTasks, taskId };
    },
    onError: (err, taskId, context) => {
      // Rollback the optimistic update if there's an error
      if (context?.previousTask) {
        queryClient.setQueryData(QUERY_KEYS.task(context.taskId), context.previousTask);
      }
      if (context?.previousTasks) {
        queryClient.setQueryData(QUERY_KEYS.tasks(), context.previousTasks);
      }
    },
    onSuccess: (result, taskId, context) => {
      // The optimistic update was already applied, so no additional action needed
      // The cache is already updated with the deletion
    },
  });
}

// Export all query keys for external use if needed
export { QUERY_KEYS };