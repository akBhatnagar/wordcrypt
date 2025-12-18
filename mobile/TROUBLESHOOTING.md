# Troubleshooting: "Unknown run configuration type FlutterRunConfigurationType"

## Quick Fix Steps

### Step 1: Verify Flutter Plugin Installation

1. **Open Android Studio**
2. Go to **File** → **Settings** (or **Android Studio** → **Preferences** on Mac)
3. Navigate to **Plugins**
4. Search for "Flutter"
5. **Check if it's installed:**
   - ✅ If installed: Make sure it's **enabled** (checkbox checked)
   - ❌ If not installed: Click **Install** → Restart IDE

### Step 2: Verify Flutter SDK Path

1. Go to **File** → **Settings** → **Languages & Frameworks** → **Flutter**
2. **Check Flutter SDK path:**
   - Should point to your Flutter installation
   - Example: `/Users/akshay/flutter` or `/Users/akshay/development/flutter`
3. If empty or wrong:
   - Click folder icon
   - Navigate to Flutter SDK directory
   - Click **Apply** → **OK**

### Step 3: Restart Android Studio

1. **Close Android Studio completely**
2. **Reopen Android Studio**
3. **Reopen the project**

### Step 4: Invalidate Caches

1. Go to **File** → **Invalidate Caches / Restart**
2. Select **Invalidate and Restart**
3. Wait for Android Studio to restart

### Step 5: Re-import Project

If still not working:

1. **Close Android Studio**
2. **Delete IDE cache files:**
   ```bash
   # On Mac
   rm -rf ~/Library/Application\ Support/Google/AndroidStudio*/caches
   
   # On Windows
   # Delete: C:\Users\YourName\.AndroidStudio*\system\caches
   ```
3. **Reopen Android Studio**
4. **File** → **Open** → Select `mobile` folder again

---

## Alternative: Run from Terminal

If Android Studio still has issues, run directly from terminal:

1. **Open Terminal** (outside Android Studio)
2. **Navigate to mobile directory:**
   ```bash
   cd /Users/akshay/Desktop/Projects/wordcrypt/mobile
   ```
3. **Check Flutter setup:**
   ```bash
   flutter doctor
   ```
4. **Get dependencies:**
   ```bash
   flutter pub get
   ```
5. **List devices:**
   ```bash
   flutter devices
   ```
6. **Run the app:**
   ```bash
   flutter run
   ```

---

## Verify Flutter Installation

Run this command to check Flutter setup:

```bash
flutter doctor -v
```

**Expected output should show:**
- ✅ Flutter (channel stable, version ...)
- ✅ Android toolchain (Android SDK ...)
- ✅ Android Studio (version ...)
- ✅ VS Code (optional)
- ✅ Connected device (if device/emulator is running)

---

## Common Issues and Solutions

### Issue: Flutter plugin not showing in Plugins

**Solution:**
1. Go to **File** → **Settings** → **Plugins**
2. Click **Marketplace** tab
3. Search "Flutter"
4. Install **Flutter** plugin (this will also install Dart)
5. Restart IDE

### Issue: Flutter SDK path is correct but still error

**Solution:**
1. Close Android Studio
2. Delete `.idea` folder in mobile directory:
   ```bash
   cd /Users/akshay/Desktop/Projects/wordcrypt/mobile
   rm -rf .idea
   ```
3. Reopen project in Android Studio
4. Let Android Studio recreate project files

### Issue: Project not recognized as Flutter project

**Solution:**
1. Make sure you opened the `mobile` folder, not the parent `wordcrypt` folder
2. Check that `pubspec.yaml` exists in the opened directory
3. Try: **File** → **Close Project** → **Open** → Select `mobile` folder

---

## Manual Run Configuration

If automatic detection fails:

1. Go to **Run** → **Edit Configurations**
2. Click **+** (plus icon)
3. Select **Flutter**
4. Set:
   - **Name:** WordCrypt
   - **Dart entrypoint:** `lib/main.dart`
   - **Working directory:** `$PROJECT_DIR$`
5. Click **OK**
6. Try running again

---

## Check Project Structure

Make sure your project structure looks like this:

```
mobile/
├── android/
├── ios/
├── lib/
│   └── main.dart    ← This should exist
├── pubspec.yaml     ← This should exist
└── test/
```

If `lib/main.dart` doesn't exist, that's the problem!

---

## Still Not Working?

Try these steps in order:

1. ✅ Verify Flutter is installed: `flutter --version`
2. ✅ Verify Flutter plugin is installed in Android Studio
3. ✅ Verify Flutter SDK path in Android Studio settings
4. ✅ Restart Android Studio
5. ✅ Invalidate caches
6. ✅ Delete `.idea` folder and re-import
7. ✅ Run from terminal: `flutter run`

---

## Need More Help?

- Flutter documentation: https://flutter.dev/docs/get-started/install
- Android Studio Flutter setup: https://flutter.dev/docs/get-started/editor?tab=androidstudio

