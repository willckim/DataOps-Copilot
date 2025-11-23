import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface BasicStats {
  row_count: number
  column_count: number
  memory_usage_mb: number
  duplicate_rows: number
  total_nulls: number
  null_percentage: number
}

export interface ColumnAnalysis {
  name: string
  dtype: string
  null_count: number
  null_percentage: number
  unique_count: number
  unique_percentage: number
  min?: number
  max?: number
  mean?: number
  median?: number
  std?: number
  avg_length?: number
  max_length?: number
  min_length?: number
  sample_values?: any[]
  min_date?: string
  max_date?: string
}

export interface QualityIssue {
  severity: string
  type: string
  column?: string
  description: string
  recommendation: string
}

export interface LLMInsights {
  insights: string
  model_used?: string
  tokens_used?: number
}

export interface ProfileResponse {
  file_name: string
  timestamp: string
  basic_stats: BasicStats
  columns: ColumnAnalysis[]
  quality_issues: QualityIssue[]
  llm_insights?: LLMInsights
  upload_id?: string
  file_size_mb?: number
  success: boolean
}

// API Functions
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export const uploadAndProfile = async (
  file: File,
  useLLM: boolean = true,
  description?: string
): Promise<ProfileResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('use_llm', useLLM.toString())
  if (description) {
    formData.append('description', description)
  }

  const response = await api.post('/data/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const deleteUpload = async (uploadId: string) => {
  const response = await api.delete(`/data/${uploadId}`)
  return response.data
}

export const listModels = async () => {
  const response = await api.get('/models')
  return response.data
}