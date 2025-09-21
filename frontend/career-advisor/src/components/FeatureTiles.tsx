'use client'

import { useState } from 'react'

export function FeatureTiles() {
  const [hoveredTile, setHoveredTile] = useState<string | null>(null)

  const tiles = [
    { id: 'onboard', title: 'Onboard', description: 'Complete your profile and set career goals', icon: '🚀', route: '/onboard', eta: '5 mins', badge: 'Start Here', difficulty: 'Beginner' },
    { id: 'skill-map', title: 'Skill Map', description: 'Visualize your skills and identify gaps', icon: '🗺️', route: '/skills', eta: '10 mins', difficulty: 'Beginner' },
    { id: 'career-paths', title: 'Career Paths', description: 'Explore personalized career roadmaps', icon: '🛤️', route: '/paths', eta: '15 mins', difficulty: 'Intermediate' },
    { id: 'learning-plan', title: 'Learning Plan', description: 'Get curated learning recommendations', icon: '📚', route: '/plan', eta: '20 mins', difficulty: 'Intermediate' },
    { id: 'interview-lab', title: 'Interview Lab', description: 'Practice with AI-powered mock interviews', icon: '🎯', route: '/interview', eta: '30 mins', badge: 'Popular', difficulty: 'Advanced' },
    { id: 'market-pulse', title: 'Market Pulse', description: 'Stay updated with industry trends', icon: '📈', route: '/market', eta: '5 mins', difficulty: 'Beginner' },
    { id: 'mentors', title: 'Mentors', description: 'Connect with industry professionals', icon: '👥', route: '/mentors', eta: '10 mins', badge: 'New', difficulty: 'Intermediate' },
    { id: 'admin', title: 'Admin', description: 'Manage your account and preferences', icon: '⚙️', route: '/admin', eta: '2 mins', difficulty: 'Beginner' },
  ]

  const handleTileClick = (route: string) => {
    window.location.href = route
  }

  const getDifficultyColor = (difficulty: string) => {
    switch(difficulty) {
      case 'Beginner': return 'text-green-400 bg-green-400/10 border-green-400/20'
      case 'Intermediate': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20'
      case 'Advanced': return 'text-red-400 bg-red-400/10 border-red-400/20'
      default: return 'text-gray-400 bg-gray-400/10 border-gray-400/20'
    }
  }

  return (
    <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Your Career Journey
            </span>
            <br />
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Starts Here
            </span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Choose your path and let AI guide you through personalized career development tools
          </p>
        </div>

        {/* Tiles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {tiles.map((tile) => (
            <div
              key={tile.id}
              onMouseEnter={() => setHoveredTile(tile.id)}
              onMouseLeave={() => setHoveredTile(null)}
              onClick={() => handleTileClick(tile.route)}
              className={`group relative cursor-pointer bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/10 hover:border-white/20 shadow-lg hover:shadow-2xl transition-all duration-300 ease-out hover:-translate-y-2 ${
                hoveredTile === tile.id ? 'shadow-cyan-500/20' : ''
              }`}
            >
              {/* Badge */}
              {tile.badge && (
                <div className="absolute -top-2 -right-2 z-10">
                  <div className="bg-gradient-to-r from-cyan-400 to-blue-500 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-lg">
                    {tile.badge}
                  </div>
                </div>
              )}

              {/* Content */}
              <div className="relative p-6 h-full flex flex-col">
                {/* Icon */}
                <div className={`text-4xl mb-4 transition-transform duration-200 ${
                  hoveredTile === tile.id ? 'scale-110 rotate-3' : ''
                }`}>
                  {tile.icon}
                </div>

                {/* Title */}
                <h3 className={`text-xl font-bold mb-2 transition-colors duration-200 ${
                  hoveredTile === tile.id ? 'text-cyan-400' : 'text-white'
                }`}>
                  {tile.title}
                </h3>

                {/* Description */}
                <p className="text-gray-400 text-sm mb-4 flex-grow leading-relaxed">
                  {tile.description}
                </p>

                {/* Meta Info */}
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-2">
                    <span className="text-gray-500">⏱️ {tile.eta}</span>
                  </div>
                  <div className={`px-2 py-1 rounded-full border text-xs font-medium ${getDifficultyColor(tile.difficulty)}`}>
                    {tile.difficulty}
                  </div>
                </div>

                {/* CTA */}
                <div className={`mt-4 pt-4 border-t border-white/10 transition-all duration-200 ${
                  hoveredTile === tile.id ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
                }`}>
                  <div className="flex items-center text-cyan-400 text-sm font-medium">
                    Get Started
                    <svg className={`ml-1 w-4 h-4 transition-transform duration-200 ${
                      hoveredTile === tile.id ? 'translate-x-1' : ''
                    }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <p className="text-gray-400 mb-6">
            Not sure where to start? Let our AI guide you.
          </p>
          <button
            onClick={() => handleTileClick('/onboard')}
            className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold rounded-xl shadow-lg border border-white/20 hover:border-white/30 hover:shadow-blue-500/30 transition-all duration-300"
          >
            🤖 AI-Guided Onboarding
          </button>
        </div>
      </div>
    </section>
  )
}
