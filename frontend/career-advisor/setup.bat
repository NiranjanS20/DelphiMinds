@echo off
echo 🚀 Installing Career Advisor Homepage Dependencies...
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Install dependencies
echo 📦 Installing npm packages...
npm install --legacy-peer-deps

REM Create .env.local if it doesn't exist
if not exist .env.local (
    echo 📝 Creating .env.local file...
    (
        echo # Next.js Environment Variables
        echo NEXT_PUBLIC_APP_URL=http://localhost:3000
    ) > .env.local
)

echo.
echo ✅ Setup complete!
echo.
echo 🎯 To start the development server:
echo    npm run dev
echo.
echo 🌐 Your app will be available at:
echo    http://localhost:3000
echo.
echo 🚀 To build for production:
echo    npm run build
echo    npm start
echo.
echo 📦 Project includes:
echo    ✓ Next.js 14 with TypeScript
echo    ✓ TailwindCSS for styling
echo    ✓ Simplified component architecture
echo    ✓ Responsive design
echo    ✓ Particle background system
echo    ✓ Interactive navigation tiles
echo    ✓ AI chat interface
echo    ✓ Glassmorphism design
echo.
pause