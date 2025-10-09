'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart3, 
  Filter, 
  SortAsc, 
  SortDesc, 
  Plus, 
  Target, 
  Clock, 
  Users, 
  Zap,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Play,
  Pause
} from 'lucide-react'

interface RoadmapPRD {
  id: string
  title: string
  description: string
  prd_type?: 'platform' | 'agent'
  status: string
  category: string
  priority_score: number
  effort_estimate: string
  business_value: number
  technical_complexity: number
  assignee?: string
  target_sprint?: string
  created_at: string
  completion_percentage?: number
}

interface RoadmapOverview {
  total_prds: number
  by_status: Record<string, number>
  by_category: Record<string, number>
  by_effort: Record<string, number>
  average_priority_score: number
  categories: Record<string, any>
  statuses: Record<string, any>
}

interface PrioritizationMatrix {
  high_value_low_complexity: RoadmapPRD[]
  high_value_high_complexity: RoadmapPRD[]
  low_value_low_complexity: RoadmapPRD[]
  low_value_high_complexity: RoadmapPRD[]
}

export default function RoadmapDashboard() {
  const [overview, setOverview] = useState<RoadmapOverview | null>(null)
  const [prds, setPrds] = useState<RoadmapPRD[]>([])
  const [matrix, setMatrix] = useState<PrioritizationMatrix | null>(null)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    category: '',
    status: '',
    effort: '',
    prdType: '',
    sortBy: 'priority_score',
    sortOrder: 'desc'
  })

  useEffect(() => {
    fetchRoadmapData()
  }, [filters])

  const fetchRoadmapData = async () => {
    try {
      const [overviewRes, prdsRes, matrixRes] = await Promise.all([
        fetch('/api/v1/prds/roadmap/overview'),
        fetch(`/api/v1/prds/roadmap/prds?${new URLSearchParams({
          category: filters.category,
          status: filters.status,
          effort: filters.effort,
          prd_type: filters.prdType,
          sort_by: filters.sortBy,
          sort_order: filters.sortOrder
        })}`),
        fetch('/api/v1/prds/roadmap/prioritization-matrix')
      ])

      if (overviewRes.ok) {
        setOverview(await overviewRes.json())
      }
      if (prdsRes.ok) {
        setPrds(await prdsRes.json())
      }
      if (matrixRes.ok) {
        setMatrix(await matrixRes.json())
      }
    } catch (error) {
      console.error('Error fetching roadmap data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    const statusColors: Record<string, string> = {
      'backlog': 'bg-gray-100 text-gray-800',
      'planned': 'bg-blue-100 text-blue-800',
      'in_progress': 'bg-yellow-100 text-yellow-800',
      'review': 'bg-purple-100 text-purple-800',
      'completed': 'bg-green-100 text-green-800',
      'cancelled': 'bg-red-100 text-red-800'
    }
    return statusColors[status] || 'bg-gray-100 text-gray-800'
  }

  const getCategoryColor = (category: string) => {
    if (!overview?.categories[category]) return 'bg-gray-100 text-gray-800'
    return `bg-[${overview.categories[category].color}] text-white`
  }

  const getEffortColor = (effort: string) => {
    const effortColors: Record<string, string> = {
      'small': 'bg-green-100 text-green-800',
      'medium': 'bg-yellow-100 text-yellow-800',
      'large': 'bg-orange-100 text-orange-800',
      'epic': 'bg-red-100 text-red-800'
    }
    return effortColors[effort] || 'bg-gray-100 text-gray-800'
  }

  const getPriorityIcon = (score: number) => {
    if (score >= 8) return <AlertCircle className="h-4 w-4 text-red-500" />
    if (score >= 6) return <TrendingUp className="h-4 w-4 text-orange-500" />
    if (score >= 4) return <Target className="h-4 w-4 text-yellow-500" />
    return <Clock className="h-4 w-4 text-gray-500" />
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <BarChart3 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p>Loading roadmap...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Product Roadmap</h1>
        <p className="text-muted-foreground mt-2">
          Manage and prioritize your PRDs for strategic product development
        </p>
      </div>

      {/* Overview Stats */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total PRDs</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{overview.total_prds}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Priority</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{overview.average_priority_score}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">In Progress</CardTitle>
              <Play className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{overview.by_status.in_progress || 0}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{overview.by_status.completed || 0}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content */}
      <Tabs defaultValue="roadmap" className="space-y-4">
        <TabsList>
          <TabsTrigger value="roadmap">Roadmap View</TabsTrigger>
          <TabsTrigger value="matrix">Prioritization Matrix</TabsTrigger>
          <TabsTrigger value="kanban">Kanban Board</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="roadmap" className="space-y-4">
          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Filter className="h-5 w-5" />
                Filters & Sorting
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Category</label>
                  <select 
                    className="w-full p-2 border rounded"
                    value={filters.category}
                    onChange={(e) => setFilters({...filters, category: e.target.value})}
                  >
                    <option value="">All Categories</option>
                    {overview?.categories && Object.entries(overview.categories).map(([key, category]) => (
                      <option key={key} value={key}>{category.name}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Status</label>
                  <select 
                    className="w-full p-2 border rounded"
                    value={filters.status}
                    onChange={(e) => setFilters({...filters, status: e.target.value})}
                  >
                    <option value="">All Statuses</option>
                    {overview?.statuses && Object.entries(overview.statuses).map(([key, status]) => (
                      <option key={key} value={key}>{status.name}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Effort</label>
                  <select 
                    className="w-full p-2 border rounded"
                    value={filters.effort}
                    onChange={(e) => setFilters({...filters, effort: e.target.value})}
                  >
                    <option value="">All Efforts</option>
                    <option value="small">Small</option>
                    <option value="medium">Medium</option>
                    <option value="large">Large</option>
                    <option value="epic">Epic</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">PRD Type</label>
                  <select 
                    className="w-full p-2 border rounded"
                    value={filters.prdType}
                    onChange={(e) => setFilters({...filters, prdType: e.target.value})}
                  >
                    <option value="">All Types</option>
                    <option value="agent">Agent</option>
                    <option value="platform">Platform</option>
                  </select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Sort By</label>
                  <select 
                    className="w-full p-2 border rounded"
                    value={filters.sortBy}
                    onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
                  >
                    <option value="priority_score">Priority Score</option>
                    <option value="created_at">Created Date</option>
                    <option value="title">Title</option>
                  </select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Order</label>
                  <Button
                    variant="outline"
                    onClick={() => setFilters({...filters, sortOrder: filters.sortOrder === 'desc' ? 'asc' : 'desc'})}
                    className="w-full"
                  >
                    {filters.sortOrder === 'desc' ? <SortDesc className="h-4 w-4" /> : <SortAsc className="h-4 w-4" />}
                    {filters.sortOrder === 'desc' ? 'Descending' : 'Ascending'}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* PRD List */}
          <div className="space-y-4">
            {prds.map((prd) => (
              <Card key={prd.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="flex items-center gap-2">
                        {prd.title}
                        {getPriorityIcon(prd.priority_score)}
                        <Badge className={getStatusColor(prd.status)}>
                          {overview?.statuses[prd.status]?.name || prd.status}
                        </Badge>
                        {prd.category && (
                          <Badge className={getCategoryColor(prd.category)}>
                            {overview?.categories[prd.category]?.name || prd.category}
                          </Badge>
                        )}
                        {prd.effort_estimate && (
                          <Badge className={getEffortColor(prd.effort_estimate)}>
                            {prd.effort_estimate}
                          </Badge>
                        )}
                      </CardTitle>
                      <CardDescription>{prd.description}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                      <span className="text-sm font-medium">Priority Score:</span>
                      <div className="text-lg font-bold">{prd.priority_score}/10</div>
                    </div>
                    <div>
                      <span className="text-sm font-medium">Business Value:</span>
                      <div className="text-lg font-bold">{prd.business_value}/10</div>
                    </div>
                    <div>
                      <span className="text-sm font-medium">Technical Complexity:</span>
                      <div className="text-lg font-bold">{prd.technical_complexity}/10</div>
                    </div>
                    <div>
                      <span className="text-sm font-medium">Assignee:</span>
                      <div className="text-sm">{prd.assignee || 'Unassigned'}</div>
                    </div>
                  </div>
                  {prd.completion_percentage !== undefined && (
                    <div className="mt-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-sm font-medium">Completion:</span>
                        <span className="text-sm text-muted-foreground">
                          {prd.completion_percentage}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${prd.completion_percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="matrix" className="space-y-4">
          {matrix && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Quick Wins */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-green-600">🚀 Quick Wins</CardTitle>
                  <CardDescription>High value, low complexity</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {matrix.high_value_low_complexity.map((prd) => (
                      <div key={prd.id} className="p-3 border rounded-lg">
                        <div className="font-medium">{prd.title}</div>
                        <div className="text-sm text-muted-foreground">
                          Value: {prd.business_value}/10 | Complexity: {prd.technical_complexity}/10
                        </div>
                      </div>
                    ))}
                    {matrix.high_value_low_complexity.length === 0 && (
                      <p className="text-muted-foreground text-center py-4">No quick wins identified</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Major Projects */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-blue-600">🎯 Major Projects</CardTitle>
                  <CardDescription>High value, high complexity</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {matrix.high_value_high_complexity.map((prd) => (
                      <div key={prd.id} className="p-3 border rounded-lg">
                        <div className="font-medium">{prd.title}</div>
                        <div className="text-sm text-muted-foreground">
                          Value: {prd.business_value}/10 | Complexity: {prd.technical_complexity}/10
                        </div>
                      </div>
                    ))}
                    {matrix.high_value_high_complexity.length === 0 && (
                      <p className="text-muted-foreground text-center py-4">No major projects identified</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Fill-ins */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-yellow-600">⚡ Fill-ins</CardTitle>
                  <CardDescription>Low value, low complexity</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {matrix.low_value_low_complexity.map((prd) => (
                      <div key={prd.id} className="p-3 border rounded-lg">
                        <div className="font-medium">{prd.title}</div>
                        <div className="text-sm text-muted-foreground">
                          Value: {prd.business_value}/10 | Complexity: {prd.technical_complexity}/10
                        </div>
                      </div>
                    ))}
                    {matrix.low_value_low_complexity.length === 0 && (
                      <p className="text-muted-foreground text-center py-4">No fill-ins identified</p>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Question Marks */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-red-600">❓ Question Marks</CardTitle>
                  <CardDescription>Low value, high complexity</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {matrix.low_value_high_complexity.map((prd) => (
                      <div key={prd.id} className="p-3 border rounded-lg">
                        <div className="font-medium">{prd.title}</div>
                        <div className="text-sm text-muted-foreground">
                          Value: {prd.business_value}/10 | Complexity: {prd.technical_complexity}/10
                        </div>
                      </div>
                    ))}
                    {matrix.low_value_high_complexity.length === 0 && (
                      <p className="text-muted-foreground text-center py-4">No question marks identified</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        <TabsContent value="kanban" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
            {overview?.statuses && Object.entries(overview.statuses).map(([statusKey, status]) => (
              <Card key={statusKey}>
                <CardHeader>
                  <CardTitle className="text-sm">{status.name}</CardTitle>
                  <CardDescription>{overview.by_status[statusKey] || 0} items</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {prds.filter(prd => prd.status === statusKey).map((prd) => (
                      <div key={prd.id} className="p-2 border rounded text-sm">
                        <div className="font-medium">{prd.title}</div>
                        <div className="text-xs text-muted-foreground">
                          {prd.effort_estimate} • {prd.priority_score}/10
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Status Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {overview?.by_status && Object.entries(overview.by_status).map(([status, count]) => (
                    <div key={status} className="flex justify-between items-center">
                      <span className="text-sm">{overview.statuses[status]?.name || status}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${(count / overview.total_prds) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Category Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {overview?.by_category && Object.entries(overview.by_category).map(([category, count]) => (
                    <div key={category} className="flex justify-between items-center">
                      <span className="text-sm">{overview.categories[category]?.name || category}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full"
                            style={{ 
                              width: `${(count / overview.total_prds) * 100}%`,
                              backgroundColor: overview.categories[category]?.color || '#6b7280'
                            }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
