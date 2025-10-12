/**
 * Custom hook for PRD operations.
 */
import { useState, useEffect, useCallback } from 'react'
import { PRD, PRDListResponse, PRDType, PRDStatus } from '@/types'
import { apiClient } from '@/lib/api'

interface UsePRDsOptions {
  skip?: number
  limit?: number
  prdType?: PRDType
  status?: PRDStatus
  autoFetch?: boolean
}

interface UsePRDsReturn {
  prds: PRD[]
  loading: boolean
  error: string | null
  total: number
  hasNext: boolean
  refetch: () => Promise<void>
  createPRD: (prdData: Partial<PRD>) => Promise<PRD | null>
  updatePRD: (id: string, prdData: Partial<PRD>) => Promise<PRD | null>
  deletePRD: (id: string) => Promise<boolean>
  uploadPRDFile: (file: File) => Promise<PRD | null>
}

export function usePRDs(options: UsePRDsOptions = {}): UsePRDsReturn {
  const {
    skip = 0,
    limit = 100,
    prdType,
    status,
    autoFetch = true
  } = options

  const [prds, setPrds] = useState<PRD[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [hasNext, setHasNext] = useState(false)

  const fetchPRDs = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await apiClient.getPRDs(skip, limit, prdType, status)
      
      if (response.success && response.data) {
        setPrds(response.data.prds)
        setTotal(response.data.total)
        setHasNext(response.data.has_next)
      } else {
        setError(response.error?.message || 'Failed to fetch PRDs')
        setPrds([])
        setTotal(0)
        setHasNext(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setPrds([])
      setTotal(0)
      setHasNext(false)
    } finally {
      setLoading(false)
    }
  }, [skip, limit, prdType, status])

  const createPRD = useCallback(async (prdData: Partial<PRD>): Promise<PRD | null> => {
    try {
      const response = await apiClient.createPRD(prdData)
      
      if (response.success && response.data) {
        setPrds(prev => [response.data!, ...prev])
        setTotal(prev => prev + 1)
        return response.data
      } else {
        setError(response.error?.message || 'Failed to create PRD')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create PRD')
      return null
    }
  }, [])

  const updatePRD = useCallback(async (id: string, prdData: Partial<PRD>): Promise<PRD | null> => {
    try {
      const response = await apiClient.updatePRD(id, prdData)
      
      if (response.success && response.data) {
        setPrds(prev => prev.map(prd => prd.id === id ? response.data! : prd))
        return response.data
      } else {
        setError(response.error?.message || 'Failed to update PRD')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update PRD')
      return null
    }
  }, [])

  const deletePRD = useCallback(async (id: string): Promise<boolean> => {
    try {
      const response = await apiClient.deletePRD(id)
      
      if (response.success) {
        setPrds(prev => prev.filter(prd => prd.id !== id))
        setTotal(prev => prev - 1)
        return true
      } else {
        setError(response.error?.message || 'Failed to delete PRD')
        return false
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete PRD')
      return false
    }
  }, [])

  const uploadPRDFile = useCallback(async (file: File): Promise<PRD | null> => {
    try {
      const response = await apiClient.uploadPRDFile(file)
      
      if (response.success && response.data) {
        setPrds(prev => [response.data!, ...prev])
        setTotal(prev => prev + 1)
        return response.data
      } else {
        setError(response.error?.message || 'Failed to upload PRD file')
        return null
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload PRD file')
      return null
    }
  }, [])

  useEffect(() => {
    if (autoFetch) {
      fetchPRDs()
    }
  }, [fetchPRDs, autoFetch])

  return {
    prds,
    loading,
    error,
    total,
    hasNext,
    refetch: fetchPRDs,
    createPRD,
    updatePRD,
    deletePRD,
    uploadPRDFile
  }
}
