import os
import hashlib
import json
import random
from datetime import date, datetime, timedelta, timezone
from flask import Flask, render_template, request, jsonify, session
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# --- Configuration ---
WORD_LIST_FILE = 'valid_words.txt'
WORD_HISTORY_FILE = 'word_history.json'
DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))

# --- In-Memory Word Storage ---
valid_words = set()
word_list = []
word_history = {}  # {date: word} - tracks used words

def load_words():
    """Load words from the text file into a set for validation and a list for selection."""
    global valid_words, word_list
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, WORD_LIST_FILE)
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) == 4 and len(set(word)) == 4:  # Ensure unique letters
                    valid_words.add(word)
                    word_list.append(word)
        
        if not word_list:
            raise ValueError("Word list is empty")
        
        # Sort for consistency
        word_list.sort()
        print(f"✓ Loaded {len(word_list)} valid words")
            
    except FileNotFoundError:
        print(f"ERROR: {WORD_LIST_FILE} not found at {file_path}")
        print("Please run generate_wordlist.py first")
        raise
    except Exception as e:
        print(f"ERROR loading words: {e}")
        raise

def load_word_history():
    """Load history of previously used daily words."""
    global word_history
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, WORD_HISTORY_FILE)
    
    try:
        with open(file_path, 'r') as f:
            word_history = json.load(f)
    except FileNotFoundError:
        word_history = {}
    except Exception as e:
        print(f"Warning: Could not load word history: {e}")
        word_history = {}

def save_word_history():
    """Save word history to file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, WORD_HISTORY_FILE)
    
    try:
        with open(file_path, 'w') as f:
            json.dump(word_history, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save word history: {e}")

def get_ist_date():
    """Get current date in IST timezone."""
    # IST is UTC+5:30
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    ist_now = datetime.now(ist_offset)
    return ist_now.date()

def get_daily_word():
    """Get the daily word - completely random but same all day.
    Ensures no repeats until all words have been used.
    Uses IST timezone for day rollover."""
    global word_history
    
    if not word_list:
        load_words()
    
    if not word_history:
        load_word_history()
    
    # Use today's date in IST
    today = get_ist_date()
    today_str = today.isoformat()
    
    # Check if we already have a word for today
    if today_str in word_history:
        return word_history[today_str]
    
    # Get set of recently used words (to avoid repeats)
    used_words = set(word_history.values())
    
    # If all words have been used, clear history (start fresh cycle)
    if len(used_words) >= len(word_list):
        print("All words used! Starting new cycle.")
        # Keep only last 100 days to maintain some variety
        cutoff_date = (today - timedelta(days=100)).isoformat()
        word_history = {d: w for d, w in word_history.items() if d >= cutoff_date}
        used_words = set(word_history.values())
        save_word_history()
    
    # Get available words (not recently used)
    available_words = [w for w in word_list if w not in used_words]
    
    if not available_words:
        # Fallback: use all words
        available_words = word_list
    
    # TRULY RANDOM selection - unpredictable
    # Use system entropy for randomness
    selected_word = random.choice(available_words)
    
    # Save to history
    word_history[today_str] = selected_word
    save_word_history()
    
    print(f"Selected daily word for {today_str}: {selected_word}")
    
    return selected_word

def get_today_key():
    """Get a unique key for today's date in IST."""
    return get_ist_date().isoformat()

# --- Game Logic ---

def check_guess(guess, answer):
    """
    Checks a guess against the answer and returns the count of
    green (correct position) and yellow (correct letter, wrong position) matches.
    """
    guess = guess.upper()
    answer = answer.upper()
    
    print(f"[DEBUG check_guess] Guess: {guess}, Answer: {answer}")  # DEBUG
    
    green = 0
    yellow = 0
    
    # Use boolean arrays to track which letters have been "used"
    answer_used = [False] * 4
    guess_used = [False] * 4
    
    # 1. First pass: Check for "Green" matches (correct letter, correct position)
    for i in range(4):
        if guess[i] == answer[i]:
            green += 1
            answer_used[i] = True
            guess_used[i] = True
    
    # 2. Second pass: Check for "Yellow" matches (correct letter, wrong position)
    for i in range(4):
        if guess_used[i]:
            continue
        
        for j in range(4):
            if answer_used[j]:
                continue
            
            if guess[i] == answer[j]:
                yellow += 1
                answer_used[j] = True
                break
    
    result = {"green": green, "yellow": yellow}
    print(f"[DEBUG check_guess] Result: {result}")  # DEBUG
    return result

# --- Session Management ---

def init_game_session():
    """Initialize or reset game session for today."""
    today_key = get_today_key()
    
    # Check if session exists and is for today
    if 'date' not in session or session.get('date') != today_key:
        # New day or first time - reset session
        session.clear()
        session['date'] = today_key
        session['guesses'] = []  # Will store {word, green, yellow}
        session['is_complete'] = False
        session['won'] = False
        session['current_row'] = 0

def get_game_state():
    """Get current game state from session."""
    init_game_session()
    return {
        'guesses': session.get('guesses', []),
        'is_complete': session.get('is_complete', False),
        'won': session.get('won', False),
        'current_row': session.get('current_row', 0)
    }

def update_game_state(guess, result, row):
    """Update game session with new guess."""
    if 'guesses' not in session:
        session['guesses'] = []
    
    # Store guess with its feedback
    session['guesses'].append({
        'word': guess,
        'green': result['green'],
        'yellow': result['yellow']
    })
    session['current_row'] = row + 1
    
    if result['win']:
        session['is_complete'] = True
        session['won'] = True
    elif row >= 7:  # Last guess (0-indexed)
        session['is_complete'] = True
        session['won'] = False
    
    session.modified = True

# --- Flask Routes ---

@app.route('/')
def home():
    """Serve the main HTML page."""
    # Initialize session if needed
    init_game_session()
    return render_template('index.html')

@app.route('/game-state', methods=['GET'])
def game_state():
    """Get current game state."""
    state = get_game_state()
    return jsonify(state)

@app.route('/guess', methods=['POST'])
def make_guess():
    """Handle a guess submission from the frontend."""
    if not valid_words:
        load_words()
    
    # Get game state
    state = get_game_state()
    
    # Check if game is already complete
    if state['is_complete']:
        return jsonify({"error": "Game already completed for today"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    guess = data.get('guess', '').upper()
    current_row = data.get('row', 0)
    
    # --- Validation ---
    
    # Validate row number
    if not isinstance(current_row, int) or current_row < 0 or current_row >= 8:
        return jsonify({"error": "Invalid row number"}), 400
    
    # Check row matches session
    if current_row != state['current_row']:
        return jsonify({"error": "Row mismatch. Please refresh the page."}), 400
    
    if len(guess) != 4:
        return jsonify({"error": "Guess must be 4 letters"}), 400
    
    if not guess.isalpha():
        return jsonify({"error": "Guess must contain only letters"}), 400
    
    # Check for duplicate letters
    if len(set(guess)) != 4:
        return jsonify({"error": "Duplicate letters not allowed"}), 400
    
    if guess not in valid_words:
        return jsonify({"error": "Not a valid word"}), 400
    
    # Check if already guessed
    guessed_words = [g['word'] if isinstance(g, dict) else g for g in state['guesses']]
    if guess in guessed_words:
        return jsonify({"error": "Word already guessed"}), 400
    
    answer = get_daily_word()
    print(f"[DEBUG /guess] Daily word: {answer}, Guess: {guess}")  # DEBUG
    
    # --- Check the guess ---
    result = check_guess(guess, answer)
    win = (result['green'] == 4)
    result['win'] = win
    print(f"[DEBUG /guess] Result before return: {result}")  # DEBUG
    
    # Check if this is the last guess
    is_last_guess = (current_row == 7)
    
    # Update session
    update_game_state(guess, result, current_row)
    
    return jsonify({
        "green": result['green'],
        "yellow": result['yellow'],
        "win": win,
        "answer": answer if (win or is_last_guess) else None
    })

# --- Error Handlers ---

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# --- Run the App ---

if __name__ == '__main__':
    load_words()
    
    if DEBUG_MODE:
        print(f"🎮 DEBUG MODE: Today's word is: {get_daily_word()}")
    
    print(f"🚀 Starting server on port {PORT}")
    app.run(debug=DEBUG_MODE, port=PORT, host='0.0.0.0')
