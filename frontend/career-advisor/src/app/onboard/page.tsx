import { motion } from 'framer-motion'
import Link from 'next/link'

export default function OnboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-bg-start to-bg-end relative">
      <div className="absolute inset-0 bg-gradient-to-br from-primary-cobalt/10 via-transparent to-accent-neon/10"></div>
      
      <div className="relative z-10 pt-24 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                Welcome to Your
              </span>
              <br />
              <span className="bg-gradient-to-r from-primary-azure to-accent-neon bg-clip-text text-transparent">
                Career Journey
              </span>
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Let's get started by understanding your goals, skills, and preferences to create a personalized career roadmap.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="bg-glass-dark backdrop-blur-xl rounded-2xl border border-white/20 p-8"
          >
            <div className="space-y-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-primary-azure to-accent-neon rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🚀</span>
                </div>
                <h2 className="text-2xl font-bold text-white mb-2">Onboarding Process</h2>
                <p className="text-gray-400">Complete these steps to unlock your personalized experience</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-glass-light rounded-xl p-6 border border-white/20">
                  <div className="text-3xl mb-3">📝</div>
                  <h3 className="text-lg font-semibold text-white mb-2">Profile Setup</h3>
                  <p className="text-gray-400 text-sm">Tell us about your background, experience, and interests</p>
                </div>
                <div className="bg-glass-light rounded-xl p-6 border border-white/20">
                  <div className="text-3xl mb-3">🎯</div>
                  <h3 className="text-lg font-semibold text-white mb-2">Goal Setting</h3>
                  <p className="text-gray-400 text-sm">Define your career objectives and timeline</p>
                </div>
                <div className="bg-glass-light rounded-xl p-6 border border-white/20">
                  <div className="text-3xl mb-3">🧠</div>
                  <h3 className="text-lg font-semibold text-white mb-2">Skills Assessment</h3>
                  <p className="text-gray-400 text-sm">Quick evaluation of your current capabilities</p>
                </div>
              </div>

              <div className="flex justify-center">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-gradient-to-r from-primary-azure to-accent-neon text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-glow-azure transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-accent-sky"
                >
                  Start Onboarding
                </motion.button>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-center mt-8"
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