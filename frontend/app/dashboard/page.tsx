'use client'

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Upload, Database, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
import { uploadAndProfile, ProfileResponse } from '@/lib/api'
import FileUpload from '@/components/features/FileUpload'
import ProfileResults from '@/components/features/ProfileResults'

export default function Dashboard() {
  const [profileResult, setProfileResult] = useState<ProfileResponse | null>(null)

  const uploadMutation = useMutation({
    mutationFn: ({ file, useLLM }: { file: File; useLLM: boolean }) =>
      uploadAndProfile(file, useLLM),
    onSuccess: (data) => {
      setProfileResult(data)
    },
  })

  const handleFileUpload = (file: File, useLLM: boolean) => {
    setProfileResult(null)
    uploadMutation.mutate({ file, useLLM })
  }

  const handleReset = () => {
    setProfileResult(null)
    uploadMutation.reset()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link href="/" className="flex items-center space-x-2 text-gray-700 hover:text-gray-900">
              <ArrowLeft className="h-5 w-5" />
              <span>Back to Home</span>
            </Link>
            <div className="flex items-center space-x-2">
              <Database className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">DataOps Copilot</span>
            </div>
            <div className="w-24" /> {/* Spacer for centering */}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!profileResult ? (
          <>
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Upload Your Data
              </h1>
              <p className="text-lg text-gray-600">
                Upload CSV, Excel, or JSON files for instant AI-powered analysis
              </p>
            </div>

            <FileUpload
              onUpload={handleFileUpload}
              isLoading={uploadMutation.isPending}
              error={uploadMutation.error?.message}
            />

            {/* Features Info */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="card text-center">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-semibold mb-2">Automatic Profiling</h3>
                <p className="text-sm text-gray-600">
                  Get instant statistics, data types, and quality metrics
                </p>
              </div>
              <div className="card text-center">
                <div className="text-3xl mb-3">🤖</div>
                <h3 className="font-semibold mb-2">LLM Insights</h3>
                <p className="text-sm text-gray-600">
                  AI-powered recommendations and business context analysis
                </p>
              </div>
              <div className="card text-center">
                <div className="text-3xl mb-3">⚡</div>
                <h3 className="font-semibold mb-2">Lightning Fast</h3>
                <p className="text-sm text-gray-600">
                  Multi-model routing ensures optimal performance
                </p>
              </div>
            </div>
          </>
        ) : (
          <ProfileResults
            result={profileResult}
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  )
}