'use client'

import { useState, useEffect } from 'react'

export function Hero() {
  const [currentFeature, setCurrentFeature] = useState(0)

  const dashboardFeatures = [
    { title: 'Career Roadmap', description: 'Personalized learning paths', color: 'from-blue-500 to-cyan-400' },
    { title: 'Skill Assessment', description: 'AI-powered evaluations', color: 'from-cyan-500 to-blue-400' },
    { title: 'Interview Prep', description: 'Mock interviews & feedback', color: 'from-indigo-500 to-blue-400' },
    { title: 'Market Insights', description: 'Real-time industry trends', color: 'from-cyan-400 to-teal-500' },
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % dashboardFeatures.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto text-center relative z-10">
        <div className="space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/10 border border-white/20 text-sm text-gray-300">
            <span className="w-2 h-2 bg-cyan-400 rounded-full mr-2 animate-pulse"></span>
            AI-Powered Career Intelligence
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
            <span className="bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent">
              Your AI Career
            </span>
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent">
              Advisor is Here
            </span>
          </h1>

          {/* Description */}
          <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Navigate your career journey with personalized insights, skill assessments, 
            and AI-powered recommendations tailored to your unique goals.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a href="/onboard">
              <button className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold text-lg rounded-xl shadow-2xl border border-white/20 hover:shadow-blue-500/30 transition-all duration-300">
                Get Started Free
                <svg className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </a>

            <button className="group inline-flex items-center px-8 py-4 bg-white/10 backdrop-blur-md text-white font-semibold text-lg rounded-xl border border-white/20 hover:border-white/30 hover:bg-white/20 transition-all duration-300">
              <svg className="mr-2 h-5 w-5 group-hover:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M15 14h.01M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2z" />
              </svg>
              Watch Demo
            </button>
          </div>
        </div>

        {/* Dashboard Preview */}
        <div className="mt-16 relative">
          <div className="relative max-w-5xl mx-auto">
            <div className="relative bg-slate-900/80 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-transparent to-cyan-500/20"></div>
              
              {/* Dashboard Header */}
              <div className="relative p-6 border-b border-white/10">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <div className="text-sm text-gray-400">Career Dashboard</div>
                </div>
              </div>

              {/* Feature Cards */}
              <div className="relative p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {dashboardFeatures.map((feature, index) => (
                    <div key={feature.title} className={`relative group transition-all duration-500 ${
                      index === currentFeature ? 'scale-105 opacity-100' : 'opacity-60'
                    }`}>
                      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:border-white/20 transition-all duration-300">
                        <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${feature.color} mb-3 flex items-center justify-center`}>
                          <div className="w-6 h-6 bg-white/90 rounded"></div>
                        </div>
                        <h3 className="text-white font-semibold text-sm mb-1">{feature.title}</h3>
                        <p className="text-gray-400 text-xs">{feature.description}</p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Progress indicators */}
                <div className="flex justify-center mt-6 space-x-2">
                  {dashboardFeatures.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentFeature(index)}
                      className={`w-2 h-2 rounded-full transition-all duration-300 ${
                        index === currentFeature ? 'bg-cyan-400' : 'bg-white/30'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
        <div className="flex flex-col items-center text-gray-400 animate-bounce">
          <span className="text-sm mb-2">Scroll to explore</span>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </div>
    </section>
  )
}