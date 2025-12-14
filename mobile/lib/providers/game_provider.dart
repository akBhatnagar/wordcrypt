import 'package:flutter/foundation.dart';
import '../models/game_state.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';

class GameProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  final StorageService _storageService = StorageService();

  GameState? _gameState;
  List<List<String>> _currentGuesses = List.generate(8, (_) => List.filled(4, ''));
  int _currentRow = 0;
  int _currentCol = 0;
  bool _isLoading = false;
  String? _errorMessage;
  Set<String> _greyedLetters = {};
  bool _isGameOver = false;
  String? _answer;

  GameState? get gameState => _gameState;
  List<List<String>> get currentGuesses => _currentGuesses;
  int get currentRow => _currentRow;
  int get currentCol => _currentCol;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Set<String> get greyedLetters => _greyedLetters;
  bool get isGameOver => _isGameOver;
  String? get answer => _answer;

  GameProvider() {
    _initialize();
  }

  Future<void> _initialize() async {
    await loadGameState();
    await loadGreyedLetters();
  }

  Future<void> loadGameState() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _gameState = await _apiService.getGameState();
      _currentRow = _gameState!.currentRow;
      _isGameOver = _gameState!.isComplete;

      // Restore previous guesses
      for (int i = 0; i < _gameState!.guesses.length; i++) {
        final guess = _gameState!.guesses[i];
        for (int j = 0; j < 4; j++) {
          _currentGuesses[i][j] = guess.word[j];
        }
      }

      if (_gameState!.isComplete) {
        _isGameOver = true;
      }
    } catch (e) {
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadGreyedLetters() async {
    _greyedLetters = await _storageService.getGreyedLetters();
    notifyListeners();
  }

  void addLetter(String letter) {
    if (_isGameOver || _currentCol >= 4) return;
    _currentGuesses[_currentRow][_currentCol] = letter.toUpperCase();
    _currentCol++;
    notifyListeners();
  }

  void removeLetter() {
    if (_currentCol > 0) {
      _currentCol--;
      _currentGuesses[_currentRow][_currentCol] = '';
      notifyListeners();
    }
  }

  Future<bool> submitGuess() async {
    if (_currentCol != 4) {
      _errorMessage = 'Not enough letters';
      notifyListeners();
      return false;
    }

    final guess = _currentGuesses[_currentRow].join('').toUpperCase();

    // Check for duplicate letters
    if (guess.split('').toSet().length != 4) {
      _errorMessage = 'Duplicate letters not allowed';
      notifyListeners();
      return false;
    }

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final result = await _apiService.submitGuess(guess, _currentRow);

      // Update greyed letters if all wrong
      if (result.green == 0 && result.yellow == 0) {
        for (final letter in guess.split('')) {
          _greyedLetters.add(letter);
        }
        await _storageService.saveGreyedLetters(_greyedLetters);
      }

      // Add to game state
      if (_gameState != null) {
        _gameState = GameState(
          guesses: [
            ..._gameState!.guesses,
            Guess(word: guess, green: result.green, yellow: result.yellow),
          ],
          isComplete: result.win || _currentRow >= 7,
          won: result.win,
          currentRow: _currentRow + 1,
        );
      }

      if (result.win || _currentRow >= 7) {
        _isGameOver = true;
        _answer = result.answer;
        await _updateStats(result.win, _currentRow + 1);
      }

      _currentRow++;
      _currentCol = 0;

      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
      return false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _updateStats(bool won, int attempts) async {
    final stats = await _storageService.getStats();
    final today = _getISTDateString();

    // Only update if this is a new game for today
    if (stats.lastPlayedDate != today) {
      stats.gamesPlayed++;

      if (won) {
        stats.gamesWon++;
        stats.guessDistribution[attempts] = (stats.guessDistribution[attempts] ?? 0) + 1;

        // Update streak
        final yesterday = _getISTDateString(DateTime.now().subtract(const Duration(days: 1)));
        if (stats.lastPlayedDate == yesterday) {
          stats.currentStreak++;
        } else {
          stats.currentStreak = 1;
        }

        if (stats.currentStreak > stats.maxStreak) {
          stats.maxStreak = stats.currentStreak;
        }
      } else {
        stats.currentStreak = 0;
      }

      stats.lastPlayedDate = today;
      await _storageService.saveStats(stats);
    }
  }

  String _getISTDateString([DateTime? date]) {
    final now = date ?? DateTime.now();
    final utcTime = now.toUtc();
    final istTime = utcTime.add(const Duration(hours: 5, minutes: 30));
    return '${istTime.year}-${istTime.month.toString().padLeft(2, '0')}-${istTime.day.toString().padLeft(2, '0')}';
  }

  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  void toggleGreyLetter(String letter) {
    if (_greyedLetters.contains(letter)) {
      _greyedLetters.remove(letter);
    } else {
      _greyedLetters.add(letter);
    }
    _storageService.saveGreyedLetters(_greyedLetters);
    notifyListeners();
  }
}

