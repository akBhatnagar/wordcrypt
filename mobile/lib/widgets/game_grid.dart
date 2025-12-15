import 'package:flutter/material.dart';
import '../providers/game_provider.dart';
import '../models/game_state.dart';
import 'package:provider/provider.dart';

class GameGrid extends StatelessWidget {
  const GameGrid({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<GameProvider>(
      builder: (context, gameProvider, _) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(8, (row) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Tiles
                  ...List.generate(4, (col) {
                    final letter = gameProvider.currentGuesses[row][col];
                    final isFilled = letter.isNotEmpty;
                    final isCurrentRow = row == gameProvider.currentRow;
                    final isCurrentCol = isCurrentRow && col == gameProvider.currentCol;

                    // Check if this row has been submitted
                    Guess? submittedGuess;
                    if (gameProvider.gameState != null &&
                        row < gameProvider.gameState!.guesses.length) {
                      submittedGuess = gameProvider.gameState!.guesses[row];
                    }

                    Color tileColor = Colors.transparent;
                    Color borderColor = isCurrentCol
                        ? Theme.of(context).colorScheme.primary
                        : Colors.grey.shade400;
                    Color textColor = Theme.of(context).brightness == Brightness.dark
                        ? Colors.white
                        : Colors.black;

                    if (submittedGuess != null) {
                      // Tile is part of a submitted guess - could add subtle background
                      // but we'll keep it simple and show feedback in circles
                    }

                    return Container(
                      width: 60,
                      height: 60,
                      margin: const EdgeInsets.symmetric(horizontal: 4.0),
                      decoration: BoxDecoration(
                        color: tileColor,
                        border: Border.all(
                          color: borderColor,
                          width: isCurrentCol ? 2.5 : 2,
                        ),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Center(
                        child: Text(
                          letter,
                          style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: textColor,
                          ),
                        ),
                      ),
                    );
                  }),
                  // Feedback area
                  Padding(
                    padding: const EdgeInsets.only(left: 12.0),
                    child: _buildFeedback(context, gameProvider, row),
                  ),
                ],
              ),
            );
          }),
        );
      },
    );
  }

  Widget _buildFeedback(BuildContext context, GameProvider gameProvider, int row) {
    if (gameProvider.gameState == null ||
        row >= gameProvider.gameState!.guesses.length) {
      return const SizedBox(width: 60);
    }

    final guess = gameProvider.gameState!.guesses[row];
    final green = guess.green;
    final yellow = guess.yellow;

    return Row(
      children: [
        _buildFeedbackCircle(context, green, Colors.green),
        const SizedBox(width: 8),
        _buildFeedbackCircle(context, yellow, Colors.amber),
      ],
    );
  }

  Widget _buildFeedbackCircle(BuildContext context, int count, Color color) {
    if (count == 0) {
      return Container(
        width: 24,
        height: 24,
        decoration: BoxDecoration(
          color: Colors.grey.shade400,
          shape: BoxShape.circle,
        ),
        child: Center(
          child: Text(
            '0',
            style: TextStyle(
              color: Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      );
    }

    return Container(
      width: 24,
      height: 24,
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
      ),
      child: Center(
        child: Text(
          count.toString(),
          style: const TextStyle(
            color: Colors.white,
            fontSize: 12,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}

