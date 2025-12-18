# Android Studio Setup Guide - WordCrypt Mobile App

Complete guide to import and run the WordCrypt Flutter app in Android Studio.

## Prerequisites

Before starting, ensure you have:

- ✅ **Android Studio** installed (latest version recommended)
- ✅ **Flutter SDK** installed and configured
- ✅ **Android SDK** installed (via Android Studio)
- ✅ **Java JDK** (version 11 or higher)

---

## Step 1: Install Flutter Plugin in Android Studio

1. Open Android Studio
2. Go to **File** → **Settings** (or **Android Studio** → **Preferences** on Mac)
3. Navigate to **Plugins**
4. Search for "Flutter"
5. Click **Install** (this will also install Dart plugin)
6. Click **Restart IDE** when prompted

---

## Step 2: Configure Flutter SDK Path

1. After restart, go to **File** → **Settings** → **Languages & Frameworks** → **Flutter**
2. Click the folder icon next to "Flutter SDK path"
3. Navigate to your Flutter installation directory
   - Example: `/Users/yourname/flutter` (Mac/Linux)
   - Example: `C:\flutter` (Windows)
4. Click **Apply** → **OK**

---

## Step 3: Import the Project

### Option A: Open Existing Project

1. Open Android Studio
2. Click **Open** (or **File** → **Open**)
3. Navigate to the mobile directory:
   ```
   /Users/akshay/Desktop/Projects/wordcrypt/mobile
   ```
4. Select the `mobile` folder
5. Click **OK**

### Option B: Import from Version Control

1. Open Android Studio
2. Click **Get from Version Control** (or **File** → **New** → **Project from Version Control**)
3. Select **Git**
4. Enter repository URL: `https://github.com/akBhatnagar/wordcrypt.git`
5. Choose directory: `/Users/akshay/Desktop/Projects/wordcrypt`
6. Click **Clone**
7. After cloning, open the `mobile` folder

---

## Step 4: Configure Android SDK

1. Android Studio will detect Flutter project and show a prompt
2. Click **Configure** if prompted
3. Or go to **File** → **Project Structure** → **SDK Location**
4. Ensure Android SDK is configured:
   - **Android SDK location:** Usually `~/Library/Android/sdk` (Mac) or `C:\Users\YourName\AppData\Local\Android\Sdk` (Windows)
5. Click **Apply** → **OK**

---

## Step 5: Install Dependencies

1. Open terminal in Android Studio (View → Tool Windows → Terminal)
2. Navigate to mobile directory:
   ```bash
   cd mobile
   ```
3. Get Flutter dependencies:
   ```bash
   flutter pub get
   ```
4. Wait for dependencies to download

---

## Step 6: Set Up Android Emulator

### Create Virtual Device:

1. Click **Tools** → **Device Manager** (or **AVD Manager**)
2. Click **Create Device**
3. Select a device (e.g., **Pixel 5**)
4. Click **Next**
5. Select a system image (e.g., **API 34 - Android 14**)
6. Click **Download** if needed, then **Next**
7. Click **Finish**

### Or Use Physical Device:

1. Enable **Developer Options** on your Android phone:
   - Go to **Settings** → **About Phone**
   - Tap **Build Number** 7 times
2. Enable **USB Debugging**:
   - Go to **Settings** → **Developer Options**
   - Enable **USB Debugging**
3. Connect phone via USB
4. Allow USB debugging when prompted

---

## Step 7: Configure API URL (Important!)

Before running, update the API URL:

1. Open: `mobile/lib/services/api_service.dart`
2. Find the `baseUrl` line:
   ```dart
   static const String baseUrl = 'https://wordcrypt.in';
   ```
3. For local testing, change to:
   ```dart
   // For Android Emulator
   static const String baseUrl = 'http://10.0.2.2:5000';
   
   // For Physical Device (use your computer's IP)
   static const String baseUrl = 'http://192.168.1.XXX:5000';
   ```
4. Save the file

**Note:** Make sure your Flask backend is running if testing locally!

---

## Step 8: Run the App

### Method 1: Using Run Button

1. Select a device from the device dropdown (top toolbar)
   - Choose your emulator or connected device
2. Click the **Run** button (green play icon) or press `Shift + F10`
3. Wait for the app to build and launch

### Method 2: Using Terminal

1. Open terminal in Android Studio
2. Navigate to mobile directory:
   ```bash
   cd mobile
   ```
3. List available devices:
   ```bash
   flutter devices
   ```
4. Run on specific device:
   ```bash
   flutter run
   ```
   Or specify device:
   ```bash
   flutter run -d <device-id>
   ```

---

## Step 9: Build Release APK (Optional)

To build a release APK for testing:

1. Open terminal
2. Navigate to mobile directory:
   ```bash
   cd mobile
   ```
3. Build release APK:
   ```bash
   flutter build apk --release
   ```
4. APK location: `mobile/build/app/outputs/flutter-apk/app-release.apk`

---

## Troubleshooting

### Issue: "Flutter SDK not found"

**Solution:**
1. Go to **File** → **Settings** → **Languages & Frameworks** → **Flutter**
2. Set Flutter SDK path correctly
3. Click **Apply** → **OK**

### Issue: "Gradle sync failed"

**Solution:**
1. Go to **File** → **Invalidate Caches / Restart**
2. Select **Invalidate and Restart**
3. After restart, run `flutter pub get` again

### Issue: "No devices found"

**Solution:**
1. Open **Device Manager** (Tools → Device Manager)
2. Create a new virtual device
3. Or connect a physical device with USB debugging enabled

### Issue: "Build failed"

**Solution:**
1. Clean the project:
   ```bash
   flutter clean
   flutter pub get
   ```
2. In Android Studio: **Build** → **Clean Project**
3. Then: **Build** → **Rebuild Project**

### Issue: "API connection error"

**Solution:**
1. Ensure backend is running (if testing locally)
2. Check API URL in `api_service.dart`
3. For emulator: Use `http://10.0.2.2:5000`
4. For physical device: Use your computer's IP address

---

## Project Structure in Android Studio

After importing, you'll see:

```
mobile/
├── android/          # Android-specific files
├── ios/              # iOS-specific files
├── lib/              # Main Dart code
│   ├── main.dart
│   ├── models/
│   ├── providers/
│   ├── screens/
│   ├── services/
│   └── widgets/
├── pubspec.yaml      # Dependencies
└── test/             # Tests
```

---

## Useful Android Studio Features

### Hot Reload
- Press `Ctrl + \` (Windows/Linux) or `Cmd + \` (Mac)
- Or click the lightning bolt icon
- Instantly see code changes without restarting

### Hot Restart
- Press `Ctrl + Shift + \` (Windows/Linux) or `Cmd + Shift + \` (Mac)
- Or click the restart icon
- Restart app with latest changes

### Debugging
1. Set breakpoints by clicking left margin
2. Click **Debug** button (bug icon)
3. Step through code execution

### Flutter Inspector
- Click **Flutter Inspector** tab
- Inspect widget tree
- View layout properties

---

## Quick Commands Reference

```bash
# Navigate to mobile directory
cd mobile

# Get dependencies
flutter pub get

# Check Flutter setup
flutter doctor

# List devices
flutter devices

# Run app
flutter run

# Run in release mode
flutter run --release

# Build APK
flutter build apk --release

# Build app bundle
flutter build appbundle --release

# Clean build
flutter clean
```

---

## Next Steps

After successfully running the app:

1. ✅ Test all features
2. ✅ Take screenshots for Play Store
3. ✅ Test on different Android versions
4. ✅ Verify API connectivity
5. ✅ Check dark/light theme switching

---

## Need Help?

- Check Flutter documentation: https://flutter.dev/docs
- Android Studio help: **Help** → **Help Topics**
- Flutter doctor: Run `flutter doctor -v` to check setup

---

**You're all set! Happy coding! 🚀**

