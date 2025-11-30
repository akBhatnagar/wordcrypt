# Changelog

## Version 2.0 - Complete Refactor (2024-11-24)

### 🎯 Critical Issues Fixed

#### 1. Word List Conflict Resolution
- **Problem**: Original `wordlist.txt` contained words with duplicate letters (BALL, BOOK, etc.) but JavaScript blocked duplicate letter input
- **Solution**: Generated new `valid_words.txt` with 5,549 words containing only unique letters
- **Impact**: All words are now playable

#### 2. Duplicate Letter Logic Consistency
- **Problem**: Frontend prevented duplicate letters but backend didn't validate
- **Solution**: Added server-side duplicate letter validation
- **Impact**: Consistent behavior across frontend and backend

### 🔒 Security Improvements

#### 3. Secure Daily Word Algorithm
- **Problem**: Simple modulo operation made daily words predictable
- **Solution**: Implemented SHA256 hash-based word selection
- **Impact**: Users cannot predict future or past words

#### 4. Debug Mode Control
- **Problem**: Debug mode always enabled, answer always logged
- **Solution**: Added `FLASK_DEBUG` environment variable, debug off by default
- **Impact**: Answer only shown when explicitly enabled

#### 5. Input Validation & Sanitization
- **Problem**: No validation of row numbers, limited input checks
- **Solution**: Comprehensive server-side validation:
  - Row number validation
  - Alphabetic character check
  - Duplicate letter detection
  - Word length validation
  - Valid word verification
- **Impact**: Prevents cheating and invalid submissions

#### 6. Session-Based State Management
- **Problem**: No game state tracking, could submit unlimited guesses
- **Solution**: Flask session-based tracking of:
  - Daily completion status
  - Previous guesses
  - Current row position
  - Win/loss state
- **Impact**: Users can only play once per day, progress persists across refreshes

### ⚙️ Configuration & Environment

#### 7. Environment Variable Support
- **Problem**: Hardcoded port (5000), no secret key configuration
- **Solution**: Added environment variables:
  - `PORT` - Custom port (default: 5000)
  - `FLASK_DEBUG` - Debug mode toggle
  - `SECRET_KEY` - Flask session secret
- **Impact**: Easy deployment and configuration

### 🚀 Performance Improvements

#### 8. In-Memory Word Storage
- **Problem**: File reads on every validation
- **Solution**: Load all words into memory at startup
- **Impact**: Faster word validation and lookup

#### 9. Expanded Word Database
- **Problem**: Only 461 words available
- **Solution**: Generated 5,549 valid words from comprehensive dictionary
- **Impact**: More variety, less word repetition

### 🎨 User Experience Improvements

#### 10. Session Persistence
- **Problem**: Page refresh lost all progress
- **Solution**: Session-based state restoration
- **Impact**: Progress survives page refreshes

#### 11. Duplicate Guess Prevention
- **Problem**: Could submit same word multiple times
- **Solution**: Server tracks submitted guesses per session
- **Impact**: Better game flow, prevents wasted attempts

#### 12. Completion Detection
- **Problem**: Could keep guessing after game end
- **Solution**: Frontend and backend track completion status
- **Impact**: Clear game-over state

### 📚 Documentation & Setup

#### 13. Requirements Documentation
- **Added**: `requirements.txt` with Flask dependency
- **Impact**: Easy environment setup

#### 14. Comprehensive README
- **Added**: Detailed setup instructions, game rules, troubleshooting
- **Impact**: Better onboarding for new users/developers

#### 15. Quick Start Script
- **Added**: `start.sh` for one-command setup and launch
- **Impact**: Simplified development workflow

#### 16. Git Ignore Configuration
- **Added**: `.gitignore` for Python, Flask, IDEs, OS files
- **Impact**: Cleaner repository

### 🧹 Code Quality

#### 17. Error Handling
- **Added**: Proper error handlers (404, 500)
- **Added**: Try-catch blocks for file operations
- **Impact**: Better error messages, more robust application

#### 18. Code Organization
- **Improved**: Separated concerns (config, game logic, routes, session management)
- **Improved**: Added comments and docstrings
- **Impact**: More maintainable codebase

#### 19. Removed Unused Code
- **Removed**: Old word list files (`wordlist.txt`, `gptwordlist.txt`, `valid_4letter_unique_words.txt`)
- **Impact**: Cleaner project structure

### 🔧 Technical Details

#### Files Modified
- `app.py` - Complete rewrite with security fixes and session management
- `static/script.js` - Added session state loading and improved error handling
- `templates/index.html` - No changes needed (already well-structured)
- `static/style.css` - No changes needed (already well-structured)

#### Files Added
- `valid_words.txt` - New comprehensive word list (5,549 words)
- `generate_wordlist.py` - Script to generate word list
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `CHANGELOG.md` - This file
- `.gitignore` - Git ignore rules
- `start.sh` - Quick start script
- `app.py.backup` - Backup of original app.py

#### Files Removed
- `wordlist.txt` - Replaced by valid_words.txt
- `gptwordlist.txt` - Replaced by valid_words.txt
- `valid_4letter_unique_words.txt` - Replaced by valid_words.txt

### 📊 Statistics

- **Word count increase**: 461 → 5,549 (12x increase)
- **Lines of code (app.py)**: 146 → 258 (77% increase for better structure)
- **Security issues fixed**: 6 critical issues
- **New features added**: Session persistence, game state API, environment config
- **Documentation pages**: 0 → 2 (README + CHANGELOG)

### 🎮 How to Use

#### Quick Start
```bash
./start.sh
```

#### Manual Start
```bash
python3 generate_wordlist.py  # First time only
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

#### With Debug Mode
```bash
export FLASK_DEBUG=True
python3 app.py
```

### 🔮 Future Enhancements (Not Implemented)

Potential improvements for future versions:
- Statistics tracking (win rate, streak, guess distribution)
- Share functionality (copy results to clipboard)
- Hard mode (must use revealed hints)
- Custom word lists
- Multiplayer/competitive mode
- Archive mode (play past dates)
- Hints system
- Achievement badges

---

## Version 1.0 - Initial Version

Original implementation with basic Wordle clone functionality for 4-letter words.
