'use client'

import Link from 'next/link'
import { Database, Sparkles, BarChart3, Zap } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-2">
              <Database className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">DataOps Copilot</span>
            </div>
            <Link href="/dashboard">
              <button className="btn-primary">
                Launch App
              </button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Powered DataOps Platform
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload messy data, get instant insights. Powered by Claude Sonnet 4.5, GPT-5 mini, and Gemini 2.0 Flash 
            with intelligent multi-model routing for enterprise-grade analytics.
          </p>
          <div className="flex justify-center space-x-4">
            <Link href="/dashboard">
              <button className="btn-primary text-lg px-8 py-3">
                Get Started
              </button>
            </Link>
            <button className="btn-secondary text-lg px-8 py-3">
              View Demo
            </button>
          </div>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <Sparkles className="h-12 w-12 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Auto Data Profiling</h3>
            <p className="text-gray-600">
              AI analyzes your data and identifies quality issues automatically
            </p>
          </div>

          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <Database className="h-12 w-12 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Smart SQL Generation</h3>
            <p className="text-gray-600">
              Ask questions in plain English, get production-ready SQL
            </p>
          </div>

          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <BarChart3 className="h-12 w-12 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Dashboard Vision</h3>
            <p className="text-gray-600">
              Upload dashboard screenshots, extract metrics and KPIs
            </p>
          </div>

          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <Zap className="h-12 w-12 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Multi-Model Routing</h3>
            <p className="text-gray-600">
              Intelligent routing across Claude, GPT-4, and Gemini
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-20 card">
          <h2 className="text-2xl font-bold text-center mb-8">Powered By Latest AI Models</h2>
          <div className="flex justify-center items-center space-x-12 flex-wrap">
            <div className="text-center">
              <div className="text-4xl mb-2">🤖</div>
              <p className="font-semibold">Claude Sonnet 4.5</p>
              <p className="text-xs text-gray-500">Complex Reasoning</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">⚡</div>
              <p className="font-semibold">GPT-5 mini</p>
              <p className="text-xs text-gray-500">Latest & Fastest</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">✨</div>
              <p className="font-semibold">Gemini 2.0 Flash</p>
              <p className="text-xs text-gray-500">FREE Preview</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">🔵</div>
              <p className="font-semibold">Azure GPT-4o-mini</p>
              <p className="text-xs text-gray-500">Enterprise Ready</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-600">
            Built with Next.js, FastAPI, and LiteLLM | Enterprise-Grade AI DataOps
          </p>
        </div>
      </footer>
    </div>
  )
}