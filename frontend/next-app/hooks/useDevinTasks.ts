/**
 * Custom hook for Devin Task operations.
 */
import { useState, useEffect, useCallback } from 'react'
import { DevinTask, DevinTaskListResponse, DevinTaskStatus } from '@/types'
import { apiClient } from '@/lib/api'

interface UseDevinTasksOptions {
  skip?: number
  limit?: number
  status?: DevinTaskStatus
  prdId?: string
  autoFetch?: boolean
}

interface UseDevinTasksReturn {
  tasks: DevinTask[]
  loading: boolean
  error: string | null
  total: number
  hasNext: boolean
  refetch: () => Promise<void>
  createTask: (taskData: Partial<DevinTask>) => Promise<DevinTask | null>
  executeTask: (id: string) => Promise<boolean>
  completeTask: (id: string, completionData: any) => Promise<DevinTask | null>
}

export function useDevinTasks(options: UseDevinTasksOptions = {}): UseDevinTasksReturn {
  const {
    skip = 0,
    limit = 100,
    status,
    prdId,
    autoFetch = true
  } = options

  const [tasks, setTasks] = useState<DevinTask[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [hasNext, setHasNext] = useState(false)

  const fetchTasks = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await apiClient.getDevinTasks(skip, limit, status, prdId)
      
      if (response.success && response.data) {
        setTasks(response.data.tasks)
        setTotal(response.data.total)
        setHasNext(response.data.has_next)
      } else {
        setError(response.error?.message || 'Failed to fetch Devin tasks')
        setTasks([])
        setTotal(0)
        setHasNext(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setTasks([])
      setTotal(0)
      setHasNext(false)
    } finally {
      setLoading(false)
    }
  }, [skip, limit, status, prdId])

  const createTask = useCallback(async (taskData: Partial<DevinTask>): Promise<DevinTask | null> => {
    try {
      const response = await apiClient.createDevinTask(taskData)
      
      if (response.success && response.data) {
        setTasks(prev => [response.data!, ...prev])
        setTotal(prev => prev + 1)
        return response.data
      } else {
        setError(response.error?.message || 'Failed to create Devin task')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create Devin task')
      return null
    }
  }, [])

  const executeTask = useCallback(async (id: string): Promise<boolean> => {
    try {
      const response = await apiClient.executeDevinTask(id)
      
      if (response.success && response.data) {
        // Update the task status in the local state
        setTasks(prev => prev.map(task => 
          task.id === id 
            ? { ...task, status: response.data!.status }
            : task
        ))
        return true
      } else {
        setError(response.error?.message || 'Failed to execute Devin task')
        return false
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to execute Devin task')
      return false
    }
  }, [])

  const completeTask = useCallback(async (id: string, completionData: any): Promise<DevinTask | null> => {
    try {
      const response = await apiClient.completeDevinTask(id, completionData)
      
      if (response.success && response.data) {
        setTasks(prev => prev.map(task => task.id === id ? response.data! : task))
        return response.data
      } else {
        setError(response.error?.message || 'Failed to complete Devin task')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to complete Devin task')
      return null
    }
  }, [])

  useEffect(() => {
    if (autoFetch) {
      fetchTasks()
    }
  }, [fetchTasks, autoFetch])

  return {
    tasks,
    loading,
    error,
    total,
    hasNext,
    refetch: fetchTasks,
    createTask,
    executeTask,
    completeTask
  }
}
