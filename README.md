# WordCrypt

A daily word puzzle game - guess the 4-letter word with unique letters in 8 tries!

## Features

- 🎯 **4-letter words** instead of 5
- 🔄 **8 attempts** to guess the daily word
- ✨ **Unique letters only** - no duplicate letters allowed
- 🌓 **Dark/Light theme** toggle
- 💾 **Session persistence** - your progress is saved
- 🎨 **Clean, modern UI** with responsive design
- 🔒 **Secure daily word** generation using cryptographic hashing

## Game Rules

1. Guess the 4-letter word in 8 tries
2. Each guess must be a valid 4-letter word with unique letters
3. After each guess, you'll see:
   - **Green circle with number**: How many letters are in the correct position
   - **Yellow circle with number**: How many letters are correct but in wrong position
   - **Grey circles with 0**: No correct letters
4. The daily word changes at midnight (same word for everyone each day)

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd wordcrypt
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the word list (if not already done):**
   ```bash
   python3 generate_wordlist.py
   ```
   This will create `valid_words.txt` with 1,348 common 4-letter words with unique letters.

### Running the Application

#### Development Mode (with debug output)

```bash
export FLASK_DEBUG=True  # On Windows: set FLASK_DEBUG=True
python3 app.py
```

The daily word will be printed to the console in debug mode.

#### Production Mode

```bash
python3 app.py
```

Or with custom port:
```bash
export PORT=8000  # On Windows: set PORT=8000
python3 app.py
```

#### Using a Custom Secret Key (Recommended for Production)

```bash
export SECRET_KEY="your-secret-key-here"  # On Windows: set SECRET_KEY=your-secret-key-here
python3 app.py
```

### Access the Game

Open your browser and navigate to:
```
http://localhost:5000
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` |
| `FLASK_DEBUG` | Enable debug mode (shows daily word) | `False` |
| `SECRET_KEY` | Flask session secret key | `dev-secret-key-change-in-production` |

## Project Structure

```
wordcrypt/
├── app.py                          # Flask backend application
├── generate_wordlist.py            # Script to generate word list
├── requirements.txt                # Python dependencies
├── valid_words.txt                 # Curated word list (1,348 words)
├── templates/
│   └── index.html                  # Main HTML template
├── static/
│   ├── script.js                   # Frontend JavaScript
│   └── style.css                   # Styling
└── README.md                       # This file
```

## How It Works

### Backend (Flask)
- Loads 1,348 common valid 4-letter words with unique letters into memory at startup
- Uses SHA256 hash of the date to deterministically select daily word
- Manages game state using Flask sessions (cookie-based)
- Validates all guesses and prevents cheating (duplicate guesses, invalid words, etc.)

### Frontend (Vanilla JavaScript)
- Interactive keyboard (on-screen + physical keyboard support)
- Real-time validation and feedback
- Theme persistence using localStorage
- Session state restoration (prevents progress loss on refresh)

### Word List
- Curated list of common, recognizable English words
- Only includes 4-letter words with unique letters (no duplicate letters)
- 1,348 valid words for daily rotation
- All words are standard dictionary words, no obscure or archaic terms

## Security Features

- ✅ Cryptographic hash-based word selection (prevents prediction)
- ✅ Server-side validation (client can't cheat)
- ✅ Session-based game state (prevents replay attacks)
- ✅ Input sanitization and validation
- ✅ Environment variable support for secrets
- ✅ Debug mode disabled by default

## Recent Improvements

All issues from the original codebase have been fixed:

1. ✅ **Word list conflict resolved** - Only words with unique letters
2. ✅ **1,348 curated words** instead of 461 - Larger pool of recognizable words
3. ✅ **In-memory word storage** - Faster than file reads
4. ✅ **Session persistence** - Progress saved across refreshes
5. ✅ **Secure daily word** - Uses SHA256 instead of simple modulo
6. ✅ **Input validation** - Comprehensive server-side checks
7. ✅ **Environment variables** - Configurable port, debug mode, secret key
8. ✅ **No answer logging** - Only in debug mode
9. ✅ **Requirements documented** - Easy setup

## Troubleshooting

### "Word list not found" error
Run the word list generator:
```bash
python3 generate_wordlist.py
```

### Session not persisting
Make sure cookies are enabled in your browser.

### Port already in use
Change the port:
```bash
export PORT=8000
python3 app.py
```

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to submit issues and enhancement requests!
# Auto-deploy test
