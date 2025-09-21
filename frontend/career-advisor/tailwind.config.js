/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0047AB', // Cobalt Blue
          50: '#E6F2FF',
          100: '#CCE6FF',
          200: '#99CCFF',
          300: '#66B2FF',
          400: '#3399FF',
          500: '#007FFF', // Azure
          600: '#0047AB', // Cobalt Blue
          700: '#003D96',
          800: '#003280',
          900: '#002766',
        },
        accent: {
          DEFAULT: '#00E5FF', // Neon Accent
          light: '#66B2FF', // Sky Accent
          dark: '#007FFF', // Azure
        },
        background: {
          start: '#001427',
          end: '#001a33',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'hero': 'clamp(3rem, 6vw, 6rem)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'particle': 'particle 20s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(0, 229, 255, 0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(0, 229, 255, 0.6)' },
        },
        particle: {
          '0%': { transform: 'translateY(100vh) translateX(0)' },
          '100%': { transform: 'translateY(-100vh) translateX(100px)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(0, 229, 255, 0.3)',
        'glow-lg': '0 0 40px rgba(0, 229, 255, 0.4)',
      },
    },
  },
  plugins: [],
}