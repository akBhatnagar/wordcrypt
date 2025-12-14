class GameState {
  final List<Guess> guesses;
  final bool isComplete;
  final bool won;
  final int currentRow;

  GameState({
    required this.guesses,
    required this.isComplete,
    required this.won,
    required this.currentRow,
  });

  factory GameState.fromJson(Map<String, dynamic> json) {
    return GameState(
      guesses: (json['guesses'] as List<dynamic>?)
              ?.map((g) => Guess.fromJson(g))
              .toList() ??
          [],
      isComplete: json['is_complete'] ?? false,
      won: json['won'] ?? false,
      currentRow: json['current_row'] ?? 0,
    );
  }
}

class Guess {
  final String word;
  final int green;
  final int yellow;

  Guess({
    required this.word,
    required this.green,
    required this.yellow,
  });

  factory Guess.fromJson(Map<String, dynamic> json) {
    return Guess(
      word: json['word'] ?? '',
      green: json['green'] ?? 0,
      yellow: json['yellow'] ?? 0,
    );
  }
}

class GuessResult {
  final int green;
  final int yellow;
  final bool win;
  final String? answer;

  GuessResult({
    required this.green,
    required this.yellow,
    required this.win,
    this.answer,
  });

  factory GuessResult.fromJson(Map<String, dynamic> json) {
    return GuessResult(
      green: json['green'] ?? 0,
      yellow: json['yellow'] ?? 0,
      win: json['win'] ?? false,
      answer: json['answer'],
    );
  }
}

