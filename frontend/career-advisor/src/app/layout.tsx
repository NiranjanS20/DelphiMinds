'use client'

import './globals.css'
import { ParticleBackground } from '@/components/ParticleBackground'

interface RootLayoutProps {
  children: any
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <head>
        <title>Career Advisor - Personalized Career & Skills Platform</title>
        <meta name="description" content="Transform your career with AI-powered insights, personalized learning paths, and comprehensive skill development tools." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="font-sans antialiased">
        <ParticleBackground />
        {children}
      </body>
    </html>
  )
}