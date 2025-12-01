# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
WordCrypt is a daily word puzzle game where players guess 4-letter words with unique letters in 8 attempts. It's a Flask web application with vanilla JavaScript frontend, featuring session persistence, cryptographic daily word selection, and dark/light themes.

## Development Commands

### Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate word list (if missing)
python3 generate_wordlist.py
```

### Running the Application
```bash
# Development mode (shows daily word in console)
export FLASK_DEBUG=True
python3 app.py

# Production mode
python3 app.py

# Quick start (automated setup)
./start.sh

# Custom port
export PORT=8000
python3 app.py
```

### Deployment
- Uses gunicorn for production (see `Procfile`)
- CI/CD configured for DigitalOcean via GitHub Actions
- Auto-deployment on push to main branch

## Architecture & Code Structure

### Backend (Flask)
- **app.py** - Main Flask application with all routes and game logic
- **Session-based state management** - Game progress stored in Flask sessions (cookie-based)
- **In-memory word storage** - 1,434 valid words loaded at startup for fast validation
- **Cryptographic word selection** - Uses date-based randomization with history tracking to prevent repeats
- **Server-side validation** - All guesses validated server-side to prevent cheating

### Frontend
- **templates/index.html** - Single-page application template
- **static/script.js** - Vanilla JavaScript game logic, keyboard handling, and API communication
- **static/style.css** - CSS with dark/light theme support
- **Mobile-responsive** - Touch-friendly virtual keyboard with long-press functionality

### Key Game Components
1. **Daily Word Generation** (`get_daily_word()`)
   - Randomly selects from available words not used recently
   - Maintains word history in `word_history.json`
   - Prevents repeats until all words are cycled through

2. **Game State Management**
   - Session persistence across page refreshes
   - Tracks guesses, completion status, and current row
   - Prevents duplicate guesses and validates game rules

3. **Guess Validation** (`check_guess()`)
   - Returns green (correct position) and yellow (correct letter, wrong position) counts
   - Implements proper Wordle-style feedback logic

### File Dependencies
- **valid_words.txt** - Curated list of 1,434 four-letter words with unique letters
- **word_history.json** - Tracks previously used daily words (auto-generated)
- **requirements.txt** - Flask==3.0.0, gunicorn==21.2.0

## Environment Variables
- `PORT` - Server port (default: 5000)
- `FLASK_DEBUG` - Enable debug mode to show daily word (default: False)
- `SECRET_KEY` - Flask session secret key (default: dev key)

## Important Implementation Details

### Word List Requirements
- All words must be exactly 4 letters
- All words must have unique letters (no duplicates)
- Words are validated both client-side and server-side

### Session Management
- Game state persists across browser refreshes
- New session created each day at midnight
- Prevents cheating through session validation

### Security Features
- Server-side guess validation prevents client manipulation
- Cryptographic daily word selection prevents prediction
- Input sanitization and comprehensive error handling

## Common Development Patterns
- Use `init_game_session()` before any game state operations
- Always validate input server-side in addition to client-side
- Session modifications require `session.modified = True`
- Error responses use consistent JSON format with `error` field

## Troubleshooting
- If "Word list not found" error occurs, run `python3 generate_wordlist.py` to create it - WordCrypt expects `valid_words.txt` to exist with 1,434 words
- Session issues typically resolve with browser cookie clearing
- For port conflicts, use `PORT` environment variable