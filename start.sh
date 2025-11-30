#!/bin/bash
# Quick start script for WordCrypt

echo "🎮 WordCrypt - Starting..."

# Check if valid_words.txt exists
if [ ! -f "valid_words.txt" ]; then
    echo "⚠️  Word list not found. Generating..."
    python3 generate_wordlist.py
    if [ $? -ne 0 ]; then
        echo "❌ Failed to generate word list"
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start the server
echo "🚀 Starting server..."
echo "📍 Access the game at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
