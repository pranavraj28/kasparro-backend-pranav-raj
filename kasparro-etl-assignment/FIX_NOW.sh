#!/bin/bash
# Quick fix script - moves files to root for GitHub

echo "🔧 Fixing file structure for Render..."

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found in current directory"
    exit 1
fi

echo "✅ Dockerfile found"
echo ""
echo "📝 INSTRUCTIONS:"
echo ""
echo "1. Go to Render Dashboard"
echo "2. Click your service → Settings"
echo "3. Find 'Root Directory' field"
echo "4. Set it to: kasparro-etl-assignment"
echo "5. Set 'Dockerfile Path' to: Dockerfile"
echo "6. Click Save"
echo "7. Go to Events → Manual Deploy"
echo ""
echo "OR if that doesn't work:"
echo ""
echo "Upload all files from kasparro-etl-assignment/ to GitHub root"
echo "using GitHub website upload feature"
