# WordCrypt Mobile App

A Flutter mobile application for the WordCrypt daily word puzzle game.

## Features

- 🎯 **4-letter word guessing** with 8 attempts
- ✨ **Unique letters only** - no duplicate letters allowed
- 🌓 **Dark/Light theme** toggle
- 📊 **Statistics tracking** - win rate, streak, guess distribution
- 💾 **Local storage** - game state and stats persist
- ⌨️ **Virtual keyboard** with QWERTY layout
- 🎨 **Modern UI** with Material Design 3

## Setup

### Prerequisites

- Flutter SDK (3.9.0 or higher)
- Dart SDK
- Android Studio / Xcode (for mobile development)
- Backend server running (see main project README)

### Installation

1. **Navigate to the mobile directory:**
   ```bash
   cd mobile
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Configure API URL:**
   
   Open `lib/services/api_service.dart` and update the `baseUrl`:
   
   - **Android Emulator**: `http://10.0.2.2:5000` (default)
   - **iOS Simulator**: `http://localhost:5000`
   - **Physical Device**: Use your computer's IP address (e.g., `http://192.168.1.100:5000`)
   - **Production**: Your deployed backend URL

4. **Run the app:**
   ```bash
   flutter run
   ```

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/
│   └── game_state.dart      # Data models
├── services/
│   ├── api_service.dart     # Backend API communication
│   └── storage_service.dart # Local storage (stats, theme)
├── providers/
│   ├── game_provider.dart   # Game state management
│   └── theme_provider.dart  # Theme management
├── screens/
│   ├── game_screen.dart     # Main game screen
│   └── stats_screen.dart    # Statistics screen
└── widgets/
    ├── game_grid.dart       # Game grid UI
    └── game_keyboard.dart   # Virtual keyboard
```

## API Endpoints

The app communicates with the Flask backend using:

- `GET /game-state` - Get current game state
- `POST /guess` - Submit a guess

See the main project README for backend setup.

## Features Implementation

### Game Grid
- 8 rows × 4 columns
- Visual feedback with green/yellow/grey circles
- Current tile highlighting

### Keyboard
- QWERTY layout
- Long-press to grey out letters
- Visual feedback for greyed letters
- Enter and Backspace keys

### Statistics
- Games played
- Win percentage
- Current streak
- Guess distribution chart

### Theme
- Light and dark modes
- Persisted in local storage
- Material Design 3 theming

## Building for Production

### Android

```bash
flutter build apk --release
# or
flutter build appbundle --release
```

### iOS

```bash
flutter build ios --release
```

## Troubleshooting

### "Failed to load game state" error

- Ensure the backend server is running
- Check the API URL in `api_service.dart`
- For physical devices, ensure your phone and computer are on the same network
- Check firewall settings

### App not connecting to backend

- Verify the backend is accessible from your device/emulator
- For Android emulator, use `10.0.2.2` instead of `localhost`
- For iOS simulator, `localhost` should work
- For physical devices, use your computer's local IP address

### Theme not persisting

- Check that `shared_preferences` package is properly installed
- Clear app data and restart if needed

## License

This project is open source and available for educational purposes.
