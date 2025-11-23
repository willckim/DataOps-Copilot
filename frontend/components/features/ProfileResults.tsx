'use client'

import { ProfileResponse } from '@/lib/api'
import { FileText, AlertTriangle, CheckCircle, RotateCcw, Database } from 'lucide-react'

interface ProfileResultsProps {
  result: ProfileResponse
  onReset: () => void
}

export default function ProfileResults({ result, onReset }: ProfileResultsProps) {
  const { basic_stats, columns, quality_issues, llm_insights, file_name } = result

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Analysis Results
          </h1>
          <p className="text-gray-600">
            File: <span className="font-medium">{file_name}</span>
          </p>
        </div>
        <button onClick={onReset} className="btn-secondary flex items-center space-x-2">
          <RotateCcw className="h-4 w-4" />
          <span>Upload New File</span>
        </button>
      </div>

      {/* Basic Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center space-x-3">
            <Database className="h-8 w-8 text-primary-600" />
            <div>
              <p className="text-sm text-gray-600">Total Rows</p>
              <p className="text-2xl font-bold text-gray-900">
                {basic_stats.row_count.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <FileText className="h-8 w-8 text-primary-600" />
            <div>
              <p className="text-sm text-gray-600">Total Columns</p>
              <p className="text-2xl font-bold text-gray-900">
                {basic_stats.column_count}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="h-8 w-8 text-yellow-600" />
            <div>
              <p className="text-sm text-gray-600">Null Values</p>
              <p className="text-2xl font-bold text-gray-900">
                {basic_stats.null_percentage.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quality Issues */}
      {quality_issues.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center space-x-2">
            <AlertTriangle className="h-6 w-6 text-yellow-600" />
            <span>Quality Issues ({quality_issues.length})</span>
          </h2>
          <div className="space-y-3">
            {quality_issues.map((issue, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-lg border ${getSeverityColor(issue.severity)}`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium mb-1">{issue.description}</p>
                    <p className="text-sm opacity-80">
                      💡 {issue.recommendation}
                    </p>
                  </div>
                  <span className="ml-4 px-2 py-1 text-xs font-semibold rounded-full bg-white bg-opacity-50">
                    {issue.severity.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Column Analysis */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Column Analysis ({columns.length})
        </h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Column
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Type
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Unique
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Nulls
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Stats
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {columns.map((col, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    {col.name}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                      {col.dtype}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {col.unique_count.toLocaleString()} ({col.unique_percentage.toFixed(1)}%)
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {col.null_count.toLocaleString()} ({col.null_percentage.toFixed(1)}%)
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {col.mean !== undefined && col.mean !== null && (
                      <span>μ: {col.mean.toFixed(2)}</span>
                    )}
                    {col.avg_length !== undefined && col.avg_length !== null && (
                      <span>avg len: {col.avg_length.toFixed(0)}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* LLM Insights */}
      {llm_insights && (
        <div className="card bg-gradient-to-br from-primary-50 to-indigo-50 border-primary-200">
          <div className="flex items-start space-x-3 mb-4">
            <div className="flex-shrink-0 bg-primary-600 text-white rounded-lg p-2">
              <span className="text-2xl">🤖</span>
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-gray-900 mb-1">
                AI Insights
              </h2>
              {llm_insights.model_used && (
                <p className="text-sm text-gray-600">
                  Powered by {llm_insights.model_used} • {llm_insights.tokens_used?.toLocaleString()} tokens
                </p>
              )}
            </div>
          </div>
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap text-gray-800">
              {llm_insights.insights}
            </div>
          </div>
        </div>
      )}

      {/* Success Message */}
      <div className="card bg-green-50 border-green-200">
        <div className="flex items-center space-x-3">
          <CheckCircle className="h-6 w-6 text-green-600" />
          <div>
            <p className="font-medium text-green-900">Analysis Complete</p>
            <p className="text-sm text-green-700">
              Your data has been successfully profiled with AI-powered insights
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}