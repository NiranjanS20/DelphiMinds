'use client'

import { useEffect } from 'react'

export function ParticleBackground() {
  useEffect(() => {
    // Simple animated background with CSS
    const style = document.createElement('style')
    style.textContent = `
      @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-30px) rotate(120deg); }
        66% { transform: translateY(15px) rotate(240deg); }
      }
      
      .particle {
        position: absolute;
        background: radial-gradient(circle, rgba(0, 127, 255, 0.8) 0%, rgba(102, 178, 255, 0.4) 50%, transparent 100%);
        border-radius: 50%;
        animation: float linear infinite;
        pointer-events: none;
      }
    `
    document.head.appendChild(style)

    // Create particles
    const particles: HTMLElement[] = []
    const particleCount = 50

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div')
      particle.className = 'particle'
      
      const size = Math.random() * 4 + 1
      particle.style.width = `${size}px`
      particle.style.height = `${size}px`
      particle.style.left = `${Math.random() * 100}%`
      particle.style.top = `${Math.random() * 100}%`
      particle.style.animationDuration = `${Math.random() * 20 + 10}s`
      particle.style.animationDelay = `${Math.random() * 20}s`
      particle.style.opacity = `${Math.random() * 0.5 + 0.1}`
      
      document.body.appendChild(particle)
      particles.push(particle)
    }

    // Cleanup function
    return () => {
      particles.forEach((particle: HTMLElement) => {
        if (particle.parentNode) {
          particle.parentNode.removeChild(particle)
        }
      })
      if (style.parentNode) {
        style.parentNode.removeChild(style)
      }
    }
  }, [])

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
      <div className="absolute inset-0 bg-gradient-to-t from-blue-900/20 via-transparent to-cyan-900/20" />
    </div>
  )
}
