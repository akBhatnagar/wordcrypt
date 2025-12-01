document.addEventListener('DOMContentLoaded', () => {
    // --- Constants ---
    const ROWS = 8;
    const COLS = 4;

    // --- State ---
    let currentRow = 0;
    let currentCol = 0;
    let guesses = Array(ROWS).fill(null).map(() => Array(COLS).fill(''));
    let submittedGuesses = []; // To track submitted words
    let isGameOver = false;
    let gameState = null; // Server game state
    let greyedLetters = new Set(); // Track greyed out letters

    // --- DOM Elements ---
    const gridElement = document.getElementById('game-grid');
    const messageElement = document.getElementById('message-area');
    const keyboardElement = document.getElementById('keyboard');
    const modalBackdrop = document.getElementById('modal-backdrop');
    const modal = document.getElementById('game-modal');
    const modalMessage = document.getElementById('modal-message');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalXBtn = document.getElementById('modal-x-btn');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const mobileInput = document.getElementById('mobile-input');

    // --- Initialization ---
    async function init() {
        createGrid();
        createKeyboard();
        addEventListeners();
        loadTheme();
        setupMobileInput();
        await loadGameState();
    }

    async function loadGameState() {
        try {
            const response = await fetch('/game-state');
            if (!response.ok) {
                console.error('Failed to load game state');
                return;
            }
            
            gameState = await response.json();
            
            // Restore greyed letters from localStorage
            loadGreyedLetters();
            
            // Restore state if game already in progress
            if (gameState.guesses && gameState.guesses.length > 0) {
                // Restore previous guesses
                restorePreviousGuesses(gameState.guesses);
                currentRow = gameState.current_row;
                
                // Game was already in progress - show completion message
                if (gameState.is_complete) {
                    isGameOver = true;
                    if (gameState.won) {
                        showModalWithTimer('You already completed today\'s puzzle!<br>Come back tomorrow for a new word.');
                    } else {
                        showModalWithTimer('You already played today!<br>Come back tomorrow for a new word.');
                    }
                }
            }
        } catch (err) {
            console.error('Error loading game state:', err);
        }
    }

    function createGrid() {
        gridElement.innerHTML = ''; // Clear previous grid
        for (let r = 0; r < ROWS; r++) {
            const rowEl = document.createElement('div');
            rowEl.className = 'grid-row';
            rowEl.id = `row-${r}`;

            const tilesEl = document.createElement('div');
            tilesEl.className = 'grid-tiles';

            for (let c = 0; c < COLS; c++) {
                const tileEl = document.createElement('div');
                tileEl.className = 'grid-tile';
                tileEl.id = `tile-${r}-${c}`;
                tilesEl.appendChild(tileEl);
            }
            rowEl.appendChild(tilesEl);

            // Add feedback area
            const feedbackEl = document.createElement('div');
            feedbackEl.className = 'feedback-area';
            feedbackEl.id = `feedback-${r}`;
            rowEl.appendChild(feedbackEl);

            gridElement.appendChild(rowEl);
        }
    }

    function createKeyboard() {
        const keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACK']
        ];

        keys.forEach(row => {
            const rowEl = document.createElement('div');
            rowEl.className = 'key-row';
            row.forEach(key => {
                const keyEl = document.createElement('button');
                keyEl.className = 'key';
                keyEl.textContent = key;
                keyEl.dataset.key = key;
                if (key === 'ENTER' || key === 'BACK') {
                    keyEl.classList.add('wide-key');
                }
                
                // Add long-press functionality for letter keys
                if (key.length === 1) {
                    let pressTimer;
                    
                    keyEl.addEventListener('mousedown', (e) => {
                        pressTimer = setTimeout(() => {
                            toggleKeyGrey(key);
                        }, 500); // 500ms for long press
                    });
                    
                    keyEl.addEventListener('mouseup', () => {
                        clearTimeout(pressTimer);
                    });
                    
                    keyEl.addEventListener('mouseleave', () => {
                        clearTimeout(pressTimer);
                    });
                    
                    // Touch events for mobile
                    keyEl.addEventListener('touchstart', (e) => {
                        pressTimer = setTimeout(() => {
                            toggleKeyGrey(key);
                        }, 500);
                    });
                    
                    keyEl.addEventListener('touchend', () => {
                        clearTimeout(pressTimer);
                    });
                    
                    keyEl.addEventListener('touchcancel', () => {
                        clearTimeout(pressTimer);
                    });
                }
                
                rowEl.appendChild(keyEl);
            });
            keyboardElement.appendChild(rowEl);
        });
    }

    // --- Event Handlers ---
    function addEventListeners() {
        // Virtual keyboard clicks
        keyboardElement.addEventListener('click', handleKeyClick);
        // Physical keyboard presses
        document.addEventListener('keydown', handleKeyPress);
        // Modal close buttons
        modalCloseBtn.addEventListener('click', closeModal);
        modalXBtn.addEventListener('click', closeModal);
        modalBackdrop.addEventListener('click', closeModal);
        themeToggleBtn.addEventListener('click', toggleTheme);
        // Tap on grid to focus mobile input
        gridElement.addEventListener('click', focusMobileInput);
    }

    function setupMobileInput() {
        // Optional: Handle mobile keyboard input if user taps on the tiles
        // But don't auto-focus, let them use on-screen keyboard
        if (/Android|webOS|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
            mobileInput.addEventListener('input', (e) => {
                const value = e.target.value.toUpperCase();
                if (value && !isGameOver) {
                    processInput(value[value.length - 1]);
                }
                // Clear input to allow continuous typing
                setTimeout(() => {
                    mobileInput.value = '';
                }, 10);
            });
        }
    }

    function focusMobileInput() {
        // Don't auto-focus on mobile - let users use on-screen keyboard
        // Only focus if they explicitly tap the hidden input area
    }

    function handleKeyClick(e) {
        if (isGameOver) return;

        const key = e.target.dataset.key;
        if (key) {
            processInput(key);
        }
    }

    function handleKeyPress(e) {
        if (isGameOver) return;

        // Use e.key and normalize to uppercase
        let key = e.key.toUpperCase();

        if (key === 'ENTER') {
            processInput('ENTER');
        } else if (key === 'BACKSPACE') {
            processInput('BACK');
        } else if (key.length === 1 && key >= 'A' && key <= 'Z') {
            processInput(key);
        }
    }

    // --- Game Actions ---
    function addLetter(key) {
        if (currentCol < COLS) {
            guesses[currentRow][currentCol] = key;
            const tile = getTile(currentRow, currentCol);
            tile.textContent = key;
            tile.classList.add('filled');
            currentCol++;
        }
    }

    function removeLetter() {
        if (currentCol > 0) {
            currentCol--;
            guesses[currentRow][currentCol] = '';
            const tile = getTile(currentRow, currentCol);
            tile.textContent = '';
            tile.classList.remove('filled');
        }
    }

    async function submitGuess() {
        if (currentCol !== COLS) {
            showMessage("Not enough letters");
            return;
        }

        const guess = guesses[currentRow].join('');

        // Prevent duplicate submissions
        if (submittedGuesses.includes(guess)) {
            showMessage("Word already guessed");
            return;
        }

        try {
            const response = await fetch('/guess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ guess: guess, row: currentRow }), // Pass current row
            });

            if (!response.ok) {
                const errorData = await response.json();
                const errorMsg = errorData.error || "An error occurred";
                
                // Check if game is already complete
                if (errorMsg.includes('already completed')) {
                    isGameOver = true;
                    showModal('You already completed today\'s puzzle!<br>Come back tomorrow.');
                    return;
                }
                
                showMessage(errorMsg);
                return;
            }

            const result = await response.json();

            // Add to submitted list
            submittedGuesses.push(guess);

            // Update feedback
            updateFeedback(result.green, result.yellow);

            // Move to next row
            currentRow++;
            currentCol = 0;

            // Check for game over
            if (result.win) {
                isGameOver = true;
                setTimeout(() => showModalWithTimer("You Win! 🎉"), 300);
            } else if (currentRow === ROWS) {
                isGameOver = true;
                // Use innerHTML for the line break
                setTimeout(() => showModalWithTimer(`You Lost!<br>The word was: ${result.answer}`), 300);
            }

        } catch (err) {
            console.error("Error submitting guess:", err);
            showMessage("Server error. Please try again.");
        }
    }

    function processInput(key) {
        if (key === 'ENTER') {
            submitGuess();
        } else if (key === 'BACK') {
            removeLetter();
        } else {
            addLetter(key);
        }
    }

    // --- Restore Previous Guesses ---
    function restorePreviousGuesses(guessHistory) {
        guessHistory.forEach((guessData, index) => {
            const word = guessData.word || guessData;
            const green = guessData.green || 0;
            const yellow = guessData.yellow || 0;
            
            // Fill in the tiles
            for (let col = 0; col < COLS; col++) {
                const tile = getTile(index, col);
                tile.textContent = word[col];
                tile.classList.add('filled');
            }
            
            // Add feedback
            updateFeedback(green, yellow, index);
            
            // Track submitted guess
            if (!submittedGuesses.includes(word)) {
                submittedGuesses.push(word);
            }
        });
    }

    // --- UI Updates ---
    function getTile(row, col) {
        return document.getElementById(`tile-${row}-${col}`);
    }

    function updateFeedback(green, yellow, rowIndex) {
        const row = rowIndex !== undefined ? rowIndex : currentRow;
        const feedbackEl = document.getElementById(`feedback-${row}`);
        feedbackEl.innerHTML = ''; // Clear old feedback

        if (green === 0 && yellow === 0) {
            // All letters are wrong - grey them out on keyboard
            const guess = guesses[row].join('');
            for (let letter of guess) {
                greyOutKey(letter);
            }
            
            // Grey for Green
            const greyGreenCircle = document.createElement('div');
            greyGreenCircle.className = 'feedback-circle grey';
            greyGreenCircle.textContent = '0';
            feedbackEl.appendChild(greyGreenCircle);

            // Grey for Yellow
            const greyYellowCircle = document.createElement('div');
            greyYellowCircle.className = 'feedback-circle grey';
            greyYellowCircle.textContent = '0';
            feedbackEl.appendChild(greyYellowCircle);
        } else {
            // Create Green circle
            const greenCircle = document.createElement('div');
            greenCircle.className = 'feedback-circle green';
            greenCircle.textContent = green;
            feedbackEl.appendChild(greenCircle);

            // Create Yellow circle
            const yellowCircle = document.createElement('div');
            yellowCircle.className = 'feedback-circle yellow';
            yellowCircle.textContent = yellow;
            feedbackEl.appendChild(yellowCircle);
        }
    }

    let messageTimer;
    function showMessage(msg) {
        messageElement.textContent = msg;

        // Clear previous timer if one exists
        if (messageTimer) {
            clearTimeout(messageTimer);
        }

        // Set new timer
        messageTimer = setTimeout(() => {
            messageElement.textContent = '';
        }, 3000);
    }

    function showModal(message) {
        modalMessage.innerHTML = message; // Use innerHTML to allow line breaks
        modalBackdrop.classList.add('show');
        modal.classList.add('show');
    }

    function showModalWithTimer(message) {
        // Calculate time until midnight
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(0, 0, 0, 0);
        
        const timerHtml = '<div id="countdown-timer" style="margin-top: 15px; font-size: 1.1rem; color: var(--color-text);"></div>';
        modalMessage.innerHTML = message + timerHtml;
        modalBackdrop.classList.add('show');
        modal.classList.add('show');
        
        // Start countdown
        const timerElement = document.getElementById('countdown-timer');
        updateCountdown(timerElement, tomorrow);
        
        // Update every second
        const interval = setInterval(() => {
            updateCountdown(timerElement, tomorrow);
        }, 1000);
        
        // Store interval to clear it later if needed
        modal.dataset.intervalId = interval;
    }

    function updateCountdown(element, targetDate) {
        const now = new Date();
        const diff = targetDate - now;
        
        if (diff <= 0) {
            element.textContent = 'New word available! Refresh the page.';
            if (element.parentElement.dataset.intervalId) {
                clearInterval(element.parentElement.dataset.intervalId);
            }
            return;
        }
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        element.textContent = `Next word in: ${hours}h ${minutes}m ${seconds}s`;
    }

    function closeModal() {
        modalBackdrop.classList.remove('show');
        modal.classList.remove('show');
        // Clear countdown interval if it exists
        if (modal.dataset.intervalId) {
            clearInterval(modal.dataset.intervalId);
            delete modal.dataset.intervalId;
        }
        // Don't reload the page - just close the modal
    }

    // --- Theme Functions ---
    function loadTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggleBtn.textContent = '☀️';
        } else {
            // Default to light
            document.body.classList.remove('dark-mode');
            themeToggleBtn.textContent = '🌙';
        }
    }

    function toggleTheme() {
        if (document.body.classList.contains('dark-mode')) {
            // Switch to light mode
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
            themeToggleBtn.textContent = '🌙';
        } else {
            // Switch to dark mode
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
            themeToggleBtn.textContent = '☀️';
        }
    }
    // --- END Theme ---

    // --- Keyboard Greying Functions ---
    function greyOutKey(letter) {
        const key = letter.toUpperCase();
        greyedLetters.add(key);
        updateKeyAppearance(key);
        saveGreyedLetters();
    }

    function toggleKeyGrey(letter) {
        const key = letter.toUpperCase();
        if (greyedLetters.has(key)) {
            greyedLetters.delete(key);
        } else {
            greyedLetters.add(key);
        }
        updateKeyAppearance(key);
        saveGreyedLetters();
    }

    function updateKeyAppearance(letter) {
        const keyElements = document.querySelectorAll(`[data-key="${letter}"]`);
        keyElements.forEach(keyEl => {
            if (greyedLetters.has(letter)) {
                keyEl.classList.add('greyed');
            } else {
                keyEl.classList.remove('greyed');
            }
        });
    }

    function saveGreyedLetters() {
        const today = new Date().toISOString().split('T')[0];
        const data = {
            date: today,
            letters: Array.from(greyedLetters)
        };
        localStorage.setItem('greyedLetters', JSON.stringify(data));
    }

    function loadGreyedLetters() {
        const saved = localStorage.getItem('greyedLetters');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                const today = new Date().toISOString().split('T')[0];
                
                // Only restore if it's from today
                if (data.date === today && Array.isArray(data.letters)) {
                    greyedLetters = new Set(data.letters);
                    // Update all key appearances
                    data.letters.forEach(letter => {
                        updateKeyAppearance(letter);
                    });
                } else {
                    // Clear old data
                    localStorage.removeItem('greyedLetters');
                }
            } catch (err) {
                console.error('Error loading greyed letters:', err);
                localStorage.removeItem('greyedLetters');
            }
        }
    }
    // --- END Keyboard Greying ---

    // --- Start the game ---
    init();
});
