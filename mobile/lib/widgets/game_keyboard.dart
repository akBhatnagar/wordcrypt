import 'package:flutter/material.dart';
import '../providers/game_provider.dart';
import 'package:provider/provider.dart';

class GameKeyboard extends StatelessWidget {
  const GameKeyboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<GameProvider>(
      builder: (context, gameProvider, _) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            _buildKeyRow(context, gameProvider, ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']),
            const SizedBox(height: 8),
            _buildKeyRow(context, gameProvider, ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']),
            const SizedBox(height: 8),
            _buildKeyRow(context, gameProvider, ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACK']),
          ],
        );
      },
    );
  }

  Widget _buildKeyRow(BuildContext context, GameProvider gameProvider, List<String> keys) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: keys.map((key) {
        if (key == 'ENTER' || key == 'BACK') {
          return _buildActionKey(context, gameProvider, key);
        } else {
          return _buildLetterKey(context, gameProvider, key);
        }
      }).toList(),
    );
  }

  Widget _buildLetterKey(BuildContext context, GameProvider gameProvider, String letter) {
    final isGreyed = gameProvider.greyedLetters.contains(letter);
    
    return GestureDetector(
      onTap: () => gameProvider.addLetter(letter),
      onLongPress: () => gameProvider.toggleGreyLetter(letter),
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 3.0, vertical: 4.0),
        padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 12.0),
        decoration: BoxDecoration(
          color: isGreyed
              ? Colors.grey.shade600
              : Theme.of(context).brightness == Brightness.dark
                  ? Colors.grey.shade800
                  : Colors.grey.shade300,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(
          letter,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: isGreyed ? Colors.grey.shade400 : null,
          ),
        ),
      ),
    );
  }

  Widget _buildActionKey(BuildContext context, GameProvider gameProvider, String key) {
    final isEnter = key == 'ENTER';
    final isEnabled = isEnter
        ? gameProvider.currentCol == 4 && !gameProvider.isLoading
        : gameProvider.currentCol > 0 && !gameProvider.isLoading;

    return GestureDetector(
      onTap: isEnabled
          ? () {
              if (isEnter) {
                gameProvider.submitGuess();
              } else {
                gameProvider.removeLetter();
              }
            }
          : null,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 3.0, vertical: 4.0),
        padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 12.0),
        decoration: BoxDecoration(
          color: isEnabled
              ? Theme.of(context).colorScheme.primary
              : Colors.grey.shade400,
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(
          isEnter ? 'ENTER' : '⌫',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: isEnabled ? Colors.white : Colors.grey.shade600,
          ),
        ),
      ),
    );
  }
}

