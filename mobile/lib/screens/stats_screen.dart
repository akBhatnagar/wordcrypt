import 'package:flutter/material.dart';
import '../services/storage_service.dart';

class StatsScreen extends StatefulWidget {
  const StatsScreen({super.key});

  @override
  State<StatsScreen> createState() => _StatsScreenState();
}

class _StatsScreenState extends State<StatsScreen> {
  final StorageService _storageService = StorageService();
  GameStats? _stats;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    final stats = await _storageService.getStats();
    setState(() {
      _stats = stats;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_stats == null) {
      return const Scaffold(
        appBar: AppBar(title: Text('Statistics')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final maxGuesses = _stats!.guessDistribution.values.reduce(
      (a, b) => a > b ? a : b,
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('Statistics'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Stats grid
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildStatItem('Played', _stats!.gamesPlayed.toString()),
                _buildStatItem('Wins', _stats!.gamesWon.toString()),
                _buildStatItem(
                  'Win %',
                  _stats!.gamesPlayed > 0
                      ? _stats!.winPercentage.round().toString()
                      : '0',
                ),
                _buildStatItem('Streak', _stats!.currentStreak.toString()),
              ],
            ),
            const SizedBox(height: 32),
            const Text(
              'Guess Distribution',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Guess distribution bars
            ...List.generate(8, (index) {
              final guessNum = index + 1;
              final count = _stats!.guessDistribution[guessNum] ?? 0;
              final percentage = maxGuesses > 0 ? (count / maxGuesses) * 100 : 0;

              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: Row(
                  children: [
                    SizedBox(
                      width: 30,
                      child: Text(
                        guessNum.toString(),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                    Expanded(
                      child: Container(
                        height: 30,
                        decoration: BoxDecoration(
                          color: Colors.grey.shade300,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Stack(
                          children: [
                            FractionallySizedBox(
                              widthFactor: percentage / 100,
                              child: Container(
                                decoration: BoxDecoration(
                                  color: Theme.of(context).colorScheme.primary,
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                alignment: Alignment.centerRight,
                                padding: const EdgeInsets.only(right: 8.0),
                                child: count > 0
                                    ? Text(
                                        count.toString(),
                                        style: const TextStyle(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      )
                                    : null,
                              ),
                            ),
                            if (count == 0)
                              Center(
                                child: Text(
                                  '0',
                                  style: TextStyle(
                                    color: Colors.grey.shade600,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildStatItem(String label, String value) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey.shade600,
          ),
        ),
      ],
    );
  }
}

