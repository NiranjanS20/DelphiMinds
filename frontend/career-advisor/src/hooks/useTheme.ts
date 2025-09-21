'use client'

import { useState, useEffect } from 'react'

export interface Theme {
  name: string
  colors: {
    primaryCobalt: string
    primaryAzure: string
    accentSky: string
    accentNeon: string
    bgStart: string
    bgEnd: string
  }
}

const themes: Record<string, Theme> = {
  default: {
    name: 'Cobalt Azure',
    colors: {
      primaryCobalt: '#0047AB',
      primaryAzure: '#007FFF',
      accentSky: '#66B2FF',
      accentNeon: '#00E5FF',
      bgStart: '#001427',
      bgEnd: '#001a33',
    },
  },
  light: {
    name: 'Light Mode',
    colors: {
      primaryCobalt: '#2563eb',
      primaryAzure: '#3b82f6',
      accentSky: '#60a5fa',
      accentNeon: '#38bdf8',
      bgStart: '#f8fafc',
      bgEnd: '#e2e8f0',
    },
  },
}

export function useTheme() {
  const [currentTheme, setCurrentTheme] = useState<string>('default')

  useEffect(() => {
    // Load theme from localStorage on mount
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme && themes[savedTheme]) {
      setCurrentTheme(savedTheme)
    }
  }, [])

  useEffect(() => {
    // Apply theme colors to CSS variables
    const theme = themes[currentTheme]
    if (theme) {
      const root = document.documentElement
      Object.entries(theme.colors).forEach(([key, value]) => {
        const cssVarName = `--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`
        root.style.setProperty(cssVarName, value)
      })
      
      // Save to localStorage
      localStorage.setItem('theme', currentTheme)
    }
  }, [currentTheme])

  const switchTheme = (themeName: string) => {
    if (themes[themeName]) {
      setCurrentTheme(themeName)
    }
  }

  return {
    currentTheme,
    theme: themes[currentTheme],
    availableThemes: Object.keys(themes),
    switchTheme,
  }
}