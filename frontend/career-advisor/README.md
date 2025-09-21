# Career Advisor Homepage

A modern, responsive homepage for a Personalized Career & Skills Advisor webapp built with Next.js, TypeScript, TailwindCSS, and simplified animations.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
# Run the setup script
setup.bat
```

**Linux/Mac:**
```bash
# Make script executable and run
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Install Dependencies**
   ```bash
   npm install --legacy-peer-deps
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Open in Browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🎯 Current Status

✅ **Completed Components:**
- Header with sticky navigation
- Hero section with animated dashboard preview
- Feature tiles with interactive hover effects
- Skill graph preview (simplified version)
- AI chat drawer with keyboard shortcuts
- Footer with newsletter signup
- Particle background system
- Responsive layout and mobile navigation

⚠️ **Known Issues:**
- Some TypeScript definitions need refinement
- Complex Framer Motion animations simplified for stability
- Particle system uses CSS animations instead of tsparticles

## 🛠 Architecture

### Simplified Component Structure
```
src/
├── app/
│   ├── layout.tsx          # Root layout with ParticleBackground
│   ├── page.tsx             # Main homepage
│   └── globals.css          # Global styles
├── components/
│   ├── Header.tsx           # Navigation with mobile support
│   ├── Hero.tsx             # Animated hero section
│   ├── FeatureTiles.tsx     # Interactive navigation tiles
│   ├── SkillGraphSimple.tsx # Simplified skill visualization
│   ├── ChatDrawer.tsx       # AI chat interface
│   ├── FooterSimple.tsx     # Comprehensive footer
│   └── ParticleBackground.tsx # CSS-based particle system
└── types/
    └── globals.d.ts         # TypeScript declarations
```

## 📦 Dependencies

### Core Framework
- `next`: Next.js 14 framework
- `react`: React 18
- `typescript`: TypeScript support

### Styling & Animation
- `tailwindcss`: Utility-first CSS framework
- `framer-motion`: Animation library
- `clsx`: Conditional class names

### Icons & UI
- `@heroicons/react`: Icon library
- `lucide-react`: Additional icons

### Particles System
- `tsparticles`: Particle background system
- `@tsparticles/react`: React integration
- `@tsparticles/engine`: Core engine
- `@tsparticles/slim`: Lightweight version

## 🎯 Available Routes

The application includes the following navigable routes:

- `/` - Homepage
- `/onboard` - User onboarding
- `/skills` - Skill mapping
- `/paths` - Career paths
- `/plan` - Learning plans
- `/interview` - Interview lab
- `/market` - Market insights
- `/mentors` - Mentor connections
- `/admin` - Admin panel

## 🎮 Interactive Features

### Chat Assistant
- **Floating Button**: Bottom-right corner with pulse animation
- **Keyboard Shortcut**: `Ctrl+K` to open chat
- **Mock Responses**: Simulated AI conversations
- **Suggested Questions**: Quick-start prompts

### Skill Graph
- **Interactive Nodes**: Click to view skill details
- **Connection Visualization**: Shows skill relationships
- **Proficiency Levels**: Color-coded skill ratings
- **Category Filtering**: Different skill types

### Navigation Tiles
- **Hover Effects**: Lift animation with glow
- **Click Navigation**: Smooth page transitions
- **Accessibility**: Keyboard navigation support
- **Badge System**: Popular/New indicators

## 🎨 Customization

### Theme Colors
Update colors in `tailwind.config.js`:

```javascript
colors: {
  'primary-cobalt': '#0047AB',
  'primary-azure': '#007FFF',
  'accent-sky': '#66B2FF',
  'accent-neon': '#00E5FF',
  // ... other colors
}
```

### Animations
Modify animations in component files using Framer Motion:

```javascript
const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
}
```

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect Repository**
   - Import project to Vercel
   - Auto-deploy on git push

2. **Environment Variables**
   - Set any required API keys
   - Configure build settings

3. **Custom Domain**
   - Add custom domain in Vercel dashboard
   - Configure DNS settings

### Other Platforms

The app is built as a static Next.js application and can be deployed to:
- Netlify
- AWS S3 + CloudFront
- GitHub Pages
- Any static hosting service

## 🧪 Testing

Run tests with:
```bash
npm test
```

## 📱 Browser Support

- Chrome/Chromium 90+
- Firefox 90+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

---

**Built with ❤️ using AI-assisted development**