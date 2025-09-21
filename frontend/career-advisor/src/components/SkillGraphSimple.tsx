'use client'

export function SkillGraphPreview() {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Your Skills
            </span>
            <br />
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Visualized
            </span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Interactive skill graph showing your competencies and learning pathways
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Interactive Graph Placeholder */}
          <div className="lg:col-span-2">
            <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6 h-96 lg:h-[500px] relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-transparent to-cyan-500/10"></div>
              
              <div className="relative h-full flex items-center justify-center">
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-3xl">🗺️</span>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">Interactive Skill Graph</h3>
                  <p className="text-gray-400 mb-4">Coming Soon - Full skill visualization</p>
                  <div className="flex justify-center space-x-4">
                    <div className="w-8 h-8 bg-blue-500 rounded-full opacity-70 animate-pulse"></div>
                    <div className="w-6 h-6 bg-cyan-400 rounded-full opacity-50 animate-pulse delay-150"></div>
                    <div className="w-10 h-10 bg-blue-600 rounded-full opacity-60 animate-pulse delay-300"></div>
                    <div className="w-4 h-4 bg-cyan-300 rounded-full opacity-80 animate-pulse delay-500"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Details Panel */}
          <div className="space-y-6">
            {/* Legend */}
            <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Skill Categories</h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-blue-500 to-cyan-400"></div>
                  <span className="text-sm text-gray-300">Frontend</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-green-500 to-emerald-400"></div>
                  <span className="text-sm text-gray-300">Backend</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-purple-500 to-pink-400"></div>
                  <span className="text-sm text-gray-300">Data</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-indigo-500 to-blue-400"></div>
                  <span className="text-sm text-gray-300">Soft Skills</span>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
              <h3 className="text-lg font-semibold text-white mb-3">Features</h3>
              <ul className="text-sm text-gray-400 space-y-2">
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Interactive skill nodes with connections</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Proficiency tracking and visualization</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Learning pathway recommendations</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Skill gap analysis and suggestions</span>
                </li>
              </ul>
            </div>

            {/* Sample Skills */}
            <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
              <h3 className="text-lg font-semibold text-white mb-3">Sample Skills</h3>
              <div className="flex flex-wrap gap-2">
                {['React', 'TypeScript', 'Node.js', 'Python', 'AWS', 'Docker'].map((skill) => (
                  <span
                    key={skill}
                    className="text-xs px-3 py-1 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-full text-cyan-300 border border-cyan-500/30"
                  >
                    {skill}
                  </span>
                ))}
              </div>
              <button className="w-full mt-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-200">
                Explore Full Graph
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}