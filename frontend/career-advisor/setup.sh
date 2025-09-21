#!/bin/bash

echo "🚀 Installing Career Advisor Homepage Dependencies..."

# Navigate to project directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing npm packages..."
npm install --legacy-peer-deps

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local file..."
    cat > .env.local << EOL
# Next.js Environment Variables
NEXT_PUBLIC_APP_URL=http://localhost:3000
EOL
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the development server:"
echo "   npm run dev"
echo ""
echo "🌐 Your app will be available at:"
echo "   http://localhost:3000"
echo ""
echo "🚀 To build for production:"
echo "   npm run build"
echo "   npm start"
echo ""
echo "📦 Project includes:"
echo "   ✓ Next.js 14 with TypeScript"
echo "   ✓ TailwindCSS for styling"
echo "   ✓ Simplified component architecture"
echo "   ✓ Responsive design"
echo "   ✓ Particle background system"
echo "   ✓ Interactive navigation tiles"
echo "   ✓ AI chat interface"
echo "   ✓ Glassmorphism design"
echo ""