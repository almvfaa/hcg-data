// frontend/hooks/useAsyncTask.ts
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/axios';

/**
 * Defines the structure of the task object returned by the backend API.
 */
type TaskStatus = {
  task_id: string;
  status: 'PENDING' | 'STARTED' | 'SUCCESS' | 'FAILURE' | 'RETRY';
  result?: any;
  error?: string;
};

/**
 * A generic hook to manage long-running asynchronous tasks with Celery.
 * It handles starting the task, polling for its status, and returning the final result.
 * 
 * @template T - The expected type of the successful task result.
 */
export const useAsyncTask = <T,>() => {
  // State to hold the ID of the currently running task.
  const [taskId, setTaskId] = useState<string | null>(null);

  // useQuery to poll the task status endpoint.
  const { data: task, error, isError: queryIsError } = useQuery<TaskStatus>({
    // The query is uniquely identified by its taskId.
    queryKey: ['asyncTask', taskId],
    // The function that fetches the task status.
    queryFn: async ()_TS_> {
      // The type assertion here is safe because of the `enabled` check below.
      const response = await apiClient.get<TaskStatus>(`/tasks/${taskId!}`);
      return response;
    },
    // This is the core of the polling logic.
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      // If the task is still running, poll every 2 seconds.
      if (status === 'PENDING' || status === 'STARTED') {
        return 2000;
      }
      // Otherwise, stop polling.
      return false;
    },
    // The query will only run if there is a valid taskId.
    enabled: !!taskId,
  });

  /**
   * Function to initiate the task.
   * @param startTaskFn - An async function that calls the API endpoint to start the task
   *                      and returns a promise that resolves to { task_id: string }.
   */
  const execute = async (startTaskFn: () => Promise<{ task_id: string }>) => {
    try {
      // Reset any previous task ID.
      setTaskId(null);
      // Call the function that starts the task on the backend.
      const { task_id } = await startTaskFn();
      // Set the new task ID, which will trigger the useQuery polling.
      setTaskId(task_id);
    } catch (e) {
      console.error("Failed to start the task:", e);
      // You might want to set an error state here.
    }
  };

  const isLoading = !!taskId && (task?.status === 'PENDING' || task?.status === 'STARTED');
  const isSuccess = task?.status === 'SUCCESS';
  const isError = queryIsError || task?.status === 'FAILURE';

  return {
    execute,
    taskId,
    task,
    isLoading,
    isSuccess,
    isError,
    error: error || (task?.error ? new Error(task.error) : null),
    // Safely cast the result to the expected generic type T.
    result: task?.result as T | undefined,
  };
};
