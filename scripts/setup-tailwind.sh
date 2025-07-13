#!/bin/bash

echo "🎨 Setting up Tailwind CSS for NetPulse Frontend..."

# Navigate to frontend directory
cd /Users/dabwitso/Documents/Work/Personal/SAAS/netpulse/netpulse_frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project to test Tailwind
echo "🔨 Building project to test Tailwind CSS..."
npm run build

echo "✅ Tailwind CSS setup complete!"
echo ""
echo "🚀 To start the development server:"
echo "   cd netpulse_frontend"
echo "   npm start"
echo ""
echo "🎯 The TailwindTest component has been added to verify styling works."
echo "   Once confirmed, you can remove it from App.js"
