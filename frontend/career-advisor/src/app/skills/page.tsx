import { motion } from 'framer-motion'
import Link from 'next/link'

export default function SkillsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-bg-start to-bg-end relative">
      <div className="absolute inset-0 bg-gradient-to-br from-primary-cobalt/10 via-transparent to-accent-neon/10"></div>
      
      <div className="relative z-10 pt-24 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                Your Skill
              </span>
              <br />
              <span className="bg-gradient-to-r from-primary-azure to-accent-neon bg-clip-text text-transparent">
                Universe
              </span>
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Visualize your skills, discover connections, and identify areas for growth with our interactive skill mapping system.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="bg-glass-dark backdrop-blur-xl rounded-2xl border border-white/20 p-8 mb-8"
          >
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-primary-azure to-accent-neon rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🗺️</span>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Interactive Skill Map</h2>
              <p className="text-gray-400">Coming Soon - Full skill visualization and analysis tools</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-glass-light rounded-xl p-6 border border-white/20 text-center">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="text-lg font-semibold text-white mb-2">Skill Assessment</h3>
                <p className="text-gray-400 text-sm">Comprehensive evaluation of your current abilities</p>
              </div>
              <div className="bg-glass-light rounded-xl p-6 border border-white/20 text-center">
                <div className="text-3xl mb-3">🔗</div>
                <h3 className="text-lg font-semibold text-white mb-2">Skill Connections</h3>
                <p className="text-gray-400 text-sm">Discover relationships between different skills</p>
              </div>
              <div className="bg-glass-light rounded-xl p-6 border border-white/20 text-center">
                <div className="text-3xl mb-3">📈</div>
                <h3 className="text-lg font-semibold text-white mb-2">Growth Tracking</h3>
                <p className="text-gray-400 text-sm">Monitor your progress over time</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-center"
          >
            <Link href="/" className="text-accent-sky hover:text-accent-neon transition-colors duration-200">
              ← Back to Homepage
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  )
}