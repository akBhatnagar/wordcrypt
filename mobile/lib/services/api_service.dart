import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/game_state.dart';

class ApiService {
  // TODO: Update this to your backend URL
  // For local development, use: 'http://10.0.2.2:5000' (Android emulator)
  // or 'http://localhost:5000' (iOS simulator)
  // For production, use your deployed backend URL
  static const String baseUrl = 'http://10.0.2.2:5000';

  Future<GameState> getGameState() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/game-state'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return GameState.fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to load game state: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching game state: $e');
    }
  }

  Future<GuessResult> submitGuess(String guess, int row) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/guess'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'guess': guess.toUpperCase(),
          'row': row,
        }),
      );

      if (response.statusCode == 200) {
        return GuessResult.fromJson(json.decode(response.body));
      } else {
        final errorData = json.decode(response.body);
        throw Exception(errorData['error'] ?? 'Failed to submit guess');
      }
    } catch (e) {
      throw Exception('Error submitting guess: $e');
    }
  }
}

