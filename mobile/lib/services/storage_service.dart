import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class StorageService {
  static const String _keyTheme = 'theme';
  static const String _keyStats = 'gameStats';
  static const String _keyGreyedLetters = 'greyedLetters';

  // Theme
  Future<bool> getIsDarkMode() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_keyTheme) ?? false;
  }

  Future<void> setIsDarkMode(bool isDark) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_keyTheme, isDark);
  }

  // Statistics
  Future<GameStats> getStats() async {
    final prefs = await SharedPreferences.getInstance();
    final statsJson = prefs.getString(_keyStats);
    if (statsJson != null) {
      try {
        return GameStats.fromJson(json.decode(statsJson));
      } catch (e) {
        return GameStats();
      }
    }
    return GameStats();
  }

  Future<void> saveStats(GameStats stats) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyStats, json.encode(stats.toJson()));
  }

  // Greyed letters
  Future<Set<String>> getGreyedLetters() async {
    final prefs = await SharedPreferences.getInstance();
    final dataJson = prefs.getString(_keyGreyedLetters);
    if (dataJson != null) {
      try {
        final data = json.decode(dataJson);
        final today = _getISTDateString();
        if (data['date'] == today && data['letters'] != null) {
          return Set<String>.from(data['letters']);
        }
      } catch (e) {
        // Ignore
      }
    }
    return <String>{};
  }

  Future<void> saveGreyedLetters(Set<String> letters) async {
    final prefs = await SharedPreferences.getInstance();
    final data = {
      'date': _getISTDateString(),
      'letters': letters.toList(),
    };
    await prefs.setString(_keyGreyedLetters, json.encode(data));
  }

  String _getISTDateString() {
    final now = DateTime.now();
    final utcTime = now.toUtc();
    final istTime = utcTime.add(const Duration(hours: 5, minutes: 30));
    return '${istTime.year}-${istTime.month.toString().padLeft(2, '0')}-${istTime.day.toString().padLeft(2, '0')}';
  }
}

class GameStats {
  int gamesPlayed;
  int gamesWon;
  int currentStreak;
  int maxStreak;
  Map<int, int> guessDistribution;
  String? lastPlayedDate;

  GameStats({
    this.gamesPlayed = 0,
    this.gamesWon = 0,
    this.currentStreak = 0,
    this.maxStreak = 0,
    Map<int, int>? guessDistribution,
    this.lastPlayedDate,
  }) : guessDistribution = guessDistribution ??
            {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0};

  Map<String, dynamic> toJson() => {
        'gamesPlayed': gamesPlayed,
        'gamesWon': gamesWon,
        'currentStreak': currentStreak,
        'maxStreak': maxStreak,
        'guessDistribution': guessDistribution,
        'lastPlayedDate': lastPlayedDate,
      };

  factory GameStats.fromJson(Map<String, dynamic> json) {
    final distribution = Map<int, int>.from(
      (json['guessDistribution'] as Map?)?.map(
            (k, v) => MapEntry(int.parse(k.toString()), v as int),
          ) ??
          {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
    );
    return GameStats(
      gamesPlayed: json['gamesPlayed'] ?? 0,
      gamesWon: json['gamesWon'] ?? 0,
      currentStreak: json['currentStreak'] ?? 0,
      maxStreak: json['maxStreak'] ?? 0,
      guessDistribution: distribution,
      lastPlayedDate: json['lastPlayedDate'],
    );
  }

  double get winPercentage {
    if (gamesPlayed == 0) return 0;
    return (gamesWon / gamesPlayed) * 100;
  }
}

