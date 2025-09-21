'use client'

import { useState } from 'react'

export function SkillGraphPreview() {
  const [selectedNode, setSelectedNode] = useState(null)
  const [hoveredNode, setHoveredNode] = useState(null)

  const mockNodes = [
    { id: 'react', label: 'React', x: 200, y: 150, category: 'frontend', proficiency: 85, connections: ['javascript', 'typescript', 'nextjs'] },
    { id: 'javascript', label: 'JavaScript', x: 100, y: 100, category: 'frontend', proficiency: 90, connections: ['react', 'nodejs'] },
    { id: 'typescript', label: 'TypeScript', x: 150, y: 50, category: 'frontend', proficiency: 75, connections: ['javascript', 'react', 'nextjs'] },
    { id: 'nextjs', label: 'Next.js', x: 300, y: 100, category: 'frontend', proficiency: 70, connections: ['react', 'typescript'] },
    { id: 'nodejs', label: 'Node.js', x: 50, y: 200, category: 'backend', proficiency: 80, connections: ['javascript'] },
    { id: 'python', label: 'Python', x: 350, y: 200, category: 'data', proficiency: 88, connections: ['ml'] },
    { id: 'ml', label: 'Machine Learning', x: 400, y: 150, category: 'data', proficiency: 60, connections: ['python'] },
  ]

  const categoryColors = {
    frontend: { bg: 'from-blue-500 to-cyan-400', border: 'border-blue-400' },
    backend: { bg: 'from-green-500 to-emerald-400', border: 'border-green-400' },
    data: { bg: 'from-purple-500 to-pink-400', border: 'border-purple-400' },
    soft: { bg: 'from-indigo-500 to-blue-400', border: 'border-indigo-400' },
  }

  const handleNodeClick = (node) => {
    setSelectedNode(selectedNode?.id === node.id ? null : node)
  }

  const getProficiencyColor = (proficiency) => {
    if (proficiency >= 80) return 'text-green-400'
    if (proficiency >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }

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
          {/* Interactive Graph */}
          <div className="lg:col-span-2">
            <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6 h-96 lg:h-[500px] relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-transparent to-cyan-500/10"></div>
              
              <svg className="w-full h-full" viewBox="0 0 450 400">
                {/* Connections */}
                <g className="connections" opacity={0.6}>
                  {mockNodes.map(node => 
                    node.connections.map(connId => {
                      const connectedNode = mockNodes.find(n => n.id === connId)
                      if (!connectedNode) return null
                      return (
                        <path
                          key={`${node.id}-${connId}`}
                          d={`M ${node.x} ${node.y} L ${connectedNode.x} ${connectedNode.y}`}
                          stroke={selectedNode && (selectedNode.id === node.id || selectedNode.id === connId) ? '#00E5FF' : 'rgba(255, 255, 255, 0.2)'}
                          strokeWidth={selectedNode && (selectedNode.id === node.id || selectedNode.id === connId) ? 3 : 1}
                          fill="none"
                        />
                      )
                    })
                  )}
                </g>

                {/* Nodes */}
                <g className="nodes">
                  {mockNodes.map((node) => {
                    const colors = categoryColors[node.category] || categoryColors.frontend
                    const isSelected = selectedNode?.id === node.id
                    const isHovered = hoveredNode?.id === node.id
                    
                    return (
                      <g key={node.id}>
                        <circle
                          cx={node.x}
                          cy={node.y}
                          r={isSelected ? 18 : isHovered ? 16 : 14}
                          fill={`url(#gradient-${node.category})`}
                          stroke={isSelected ? '#00E5FF' : 'rgba(255, 255, 255, 0.3)'}
                          strokeWidth={isSelected ? 3 : 1}
                          className="cursor-pointer transition-all duration-200 hover:scale-110"
                          onClick={() => handleNodeClick(node)}
                          onMouseEnter={() => setHoveredNode(node)}
                          onMouseLeave={() => setHoveredNode(null)}
                        />
                        
                        <text
                          x={node.x}
                          y={node.y + 30}
                          textAnchor="middle"
                          className="text-xs fill-white font-medium"
                        >
                          {node.label}
                        </text>
                      </g>
                    )
                  })}
                </g>

                {/* Gradient definitions */}
                <defs>
                  {Object.entries(categoryColors).map(([category, colors]) => (
                    <linearGradient key={category} id={`gradient-${category}`} x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#3B82F6" />
                      <stop offset="100%" stopColor="#06B6D4" />
                    </linearGradient>
                  ))}
                </defs>
              </svg>
            </div>
          </div>

          {/* Skill Details Panel */}
          <div className="space-y-6">
            {/* Legend */}
            <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Skill Categories</h3>
              <div className="space-y-3">
                {Object.entries(categoryColors).map(([category, colors]) => (
                  <div key={category} className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full bg-gradient-to-r ${colors.bg}`}></div>
                    <span className="text-sm text-gray-300 capitalize">{category}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Selected Node Details */}
            {selectedNode && (
              <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className={`w-6 h-6 rounded-full bg-gradient-to-r ${categoryColors[selectedNode.category]?.bg || categoryColors.frontend.bg}`}></div>
                  <h3 className="text-xl font-semibold text-white">{selectedNode.label}</h3>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-400">Proficiency</span>
                      <span className={`font-semibold ${getProficiencyColor(selectedNode.proficiency)}`}>
                        {selectedNode.proficiency}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full transition-all duration-800"
                        style={{ width: `${selectedNode.proficiency}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <span className="text-sm text-gray-400 block mb-2">Connected Skills</span>
                    <div className="flex flex-wrap gap-2">
                      {selectedNode.connections.map(connId => {
                        const connectedNode = mockNodes.find(n => n.id === connId)
                        return connectedNode ? (
                          <span
                            key={connId}
                            className="text-xs px-2 py-1 bg-white/10 rounded-full text-gray-300 border border-white/20"
                          >
                            {connectedNode.label}
                          </span>
                        ) : null
                      })}
                    </div>
                  </div>

                  <div className="pt-4 border-t border-white/10">
                    <button className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-200">
                      Improve This Skill
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Instructions */}
            {!selectedNode && (
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
                <h3 className="text-lg font-semibold text-white mb-3">How to Use</h3>
                <ul className="text-sm text-gray-400 space-y-2">
                  <li className="flex items-start space-x-2">
                    <span className="text-cyan-400 mt-1">•</span>
                    <span>Click on any skill node to view details</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-cyan-400 mt-1">•</span>
                    <span>Connected skills show learning pathways</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-cyan-400 mt-1">•</span>
                    <span>Colors represent different skill categories</span>
                  </li>
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}