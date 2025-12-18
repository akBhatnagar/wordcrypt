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
WORD_LIST_FILE = 'valid_words.txt'  # All valid words for guesses
COMMON_WORDS_FILE = 'common_words.txt'  # Common words for daily answers
DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))

# --- In-Memory Word Storage ---
valid_words = set()  # All valid words (for guess validation)
common_words = []  # Common words only (for daily word selection)

# Deterministic daily cycle (avoids cross-worker randomness / file races in production)
_daily_cycle = None  # list[str]
_daily_cycle_seed = None  # str

def load_words():
    """Load words from text files - valid words for guessing and common words for daily answers."""
    global valid_words, common_words
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load all valid words (for guess validation)
    valid_path = os.path.join(base_dir, WORD_LIST_FILE)
    try:
        with open(valid_path, 'r') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) == 4 and len(set(word)) == 4:  # Ensure unique letters
                    valid_words.add(word)
        
        if not valid_words:
            raise ValueError("Valid words list is empty")
        
        print(f"✓ Loaded {len(valid_words)} valid words for guessing")
            
    except FileNotFoundError:
        print(f"ERROR: {WORD_LIST_FILE} not found at {valid_path}")
        raise
    except Exception as e:
        print(f"ERROR loading valid words: {e}")
        raise
    
    # Load common words (for daily word selection)
    common_path = os.path.join(base_dir, COMMON_WORDS_FILE)
    try:
        with open(common_path, 'r') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) == 4 and len(set(word)) == 4:
                    common_words.append(word)
        
        if not common_words:
            raise ValueError("Common words list is empty")
        
        # Sort for consistency
        common_words.sort()
        print(f"✓ Loaded {len(common_words)} common words for daily answers")
            
    except FileNotFoundError:
        print(f"ERROR: {COMMON_WORDS_FILE} not found at {common_path}")
        print("Falling back to using all valid words")
        # Fallback: use valid_words if common_words.txt doesn't exist
        common_words = sorted(list(valid_words))
    except Exception as e:
        print(f"ERROR loading common words: {e}")
        # Fallback: use valid_words
        common_words = sorted(list(valid_words))

def _compute_daily_cycle_seed() -> str:
    """
    Compute a stable seed for daily-word rotation.
    Uses SECRET_KEY so the sequence isn't trivially guessable, but remains deterministic.
    """
    return os.environ.get('DAILY_WORD_SEED') or app.secret_key

def _get_daily_cycle():
    """Get a deterministic shuffled cycle of common_words (stable across workers)."""
    global _daily_cycle, _daily_cycle_seed
    if not common_words:
        load_words()

    seed = _compute_daily_cycle_seed()
    if _daily_cycle is None or _daily_cycle_seed != seed or len(_daily_cycle) != len(common_words):
        # Stable shuffle based on seed
        seed_int = int(hashlib.sha256(seed.encode('utf-8')).hexdigest(), 16)
        rng = random.Random(seed_int)
        cycle = list(common_words)
        rng.shuffle(cycle)
        _daily_cycle = cycle
        _daily_cycle_seed = seed
    return _daily_cycle

def get_ist_date():
    """Get current date in IST timezone."""
    # IST is UTC+5:30
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    ist_now = datetime.now(ist_offset)
    return ist_now.date()

def get_daily_word():
    """
    Get the daily word (deterministic, stable across workers).
    - Uses IST timezone for day rollover
    - Uses a seeded shuffle of common_words so there are no repeats until the list cycles
    - Avoids writing/reading shared files, preventing session resets in multi-worker deployments
    """
    cycle = _get_daily_cycle()
    if not cycle:
        raise ValueError("Common words list is empty")

    today = get_ist_date()
    idx = today.toordinal() % len(cycle)
    return cycle[idx]

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
    
    return {"green": green, "yellow": yellow}

# --- Session Management ---

def init_game_session():
    """Initialize or reset game session for today.
    Also validates that session is for the current daily word."""
    today_key = get_today_key()
    daily_word = get_daily_word()
    
    # Check if session needs to be reset
    needs_reset = False
    
    if 'date' not in session or session.get('date') != today_key:
        # New day or first time
        needs_reset = True
    elif 'daily_word' not in session or session.get('daily_word') != daily_word:
        # Date matches but word changed (should be extremely rare with deterministic daily word)
        # This prevents showing stale feedback from a different word
        print(f"Session word mismatch: session={session.get('daily_word')}, actual={daily_word}. Resetting.")
        needs_reset = True
    
    if needs_reset:
        # Reset session
        session.clear()
        session['date'] = today_key
        session['daily_word'] = daily_word  # Store the word to validate later
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

@app.route('/privacy-policy')
def privacy_policy():
    """Serve the privacy policy page."""
    return render_template('privacy_policy.html')

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
    
    # Check row matches session (return sync info instead of forcing refresh)
    if current_row != state['current_row']:
        return jsonify({
            "error": "Row mismatch",
            "expected_row": state['current_row'],
            "state": state
        }), 409
    
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
    
    # --- Check the guess ---
    result = check_guess(guess, answer)
    win = (result['green'] == 4)
    result['win'] = win
    
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
