import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/game_provider.dart';
import '../providers/theme_provider.dart';
import '../widgets/game_grid.dart';
import '../widgets/game_keyboard.dart';
import '../screens/stats_screen.dart';
import '../services/storage_service.dart';

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  Timer? _errorTimer;
  bool _hasShownGameOverDialog = false;

  @override
  void dispose() {
    _errorTimer?.cancel();
    super.dispose();
  }

  void _showError(String? error) {
    if (error == null) return;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(error),
        duration: const Duration(seconds: 3),
        backgroundColor: Colors.red,
      ),
    );

    final gameProvider = Provider.of<GameProvider>(context, listen: false);
    _errorTimer = Timer(const Duration(seconds: 3), () {
      gameProvider.clearError();
    });
  }

  void _showGameOverDialog(GameProvider gameProvider) {
    if (_hasShownGameOverDialog) return;
    
    final won = gameProvider.gameState?.won ?? false;
    final answer = gameProvider.answer;

    _hasShownGameOverDialog = true;
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => GameOverDialog(won: won, answer: answer),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('WordCrypt'),
        actions: [
          IconButton(
            icon: const Icon(Icons.bar_chart),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const StatsScreen()),
              );
            },
          ),
          Consumer<ThemeProvider>(
            builder: (context, themeProvider, _) {
              return IconButton(
                icon: Icon(
                  themeProvider.isDarkMode ? Icons.light_mode : Icons.dark_mode,
                ),
                onPressed: () => themeProvider.toggleTheme(),
              );
            },
          ),
        ],
      ),
      body: Consumer<GameProvider>(
        builder: (context, gameProvider, _) {
          // Show error if any
          if (gameProvider.errorMessage != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              _showError(gameProvider.errorMessage);
            });
          }

          // Show game over dialog
          if (gameProvider.isGameOver && 
              gameProvider.gameState?.isComplete == true &&
              !_hasShownGameOverDialog) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              _showGameOverDialog(gameProvider);
            });
          }
          
          // Reset dialog flag if game is not over
          if (!gameProvider.isGameOver) {
            _hasShownGameOverDialog = false;
          }

          if (gameProvider.isLoading && gameProvider.gameState == null) {
            return const Center(child: CircularProgressIndicator());
          }

          return SafeArea(
            child: Column(
              children: [
                const SizedBox(height: 20),
                const Text(
                  'Guess the 4-letter word in 8 tries',
                  style: TextStyle(fontSize: 16),
                ),
                const SizedBox(height: 20),
                Expanded(
                  child: SingleChildScrollView(
                    child: GameGrid(),
                  ),
                ),
                const SizedBox(height: 20),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: GameKeyboard(),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class GameOverDialog extends StatefulWidget {
  final bool won;
  final String? answer;

  const GameOverDialog({super.key, required this.won, this.answer});

  @override
  State<GameOverDialog> createState() => _GameOverDialogState();
}

class _GameOverDialogState extends State<GameOverDialog> {
  String _countdown = '';

  @override
  void initState() {
    super.initState();
    _updateCountdown();
    Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) {
        _updateCountdown();
      } else {
        timer.cancel();
      }
    });
  }

  void _updateCountdown() {
    final now = DateTime.now();
    final utcTime = now.toUtc();
    final istTime = utcTime.add(const Duration(hours: 5, minutes: 30));
    
    final tomorrow = DateTime(istTime.year, istTime.month, istTime.day + 1);
    final nextMidnight = tomorrow.subtract(const Duration(hours: 5, minutes: 30));
    final nextMidnightLocal = nextMidnight.toLocal();
    
    final diff = nextMidnightLocal.difference(now);
    
    if (diff.isNegative) {
      setState(() {
        _countdown = 'New word available!';
      });
      return;
    }
    
    final hours = diff.inHours;
    final minutes = diff.inMinutes.remainder(60);
    final seconds = diff.inSeconds.remainder(60);
    
    setState(() {
      _countdown = 'Next word in: ${hours}h ${minutes}m ${seconds}s';
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(widget.won ? 'You Win! 🎉' : 'You Lost!'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (!widget.won && widget.answer != null)
            Text('The word was: ${widget.answer}'),
          const SizedBox(height: 16),
          Text(
            _countdown,
            style: const TextStyle(fontSize: 14),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Close'),
        ),
      ],
    );
  }
}

