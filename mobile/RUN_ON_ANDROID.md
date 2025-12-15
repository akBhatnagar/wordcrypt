# Running WordCrypt on Android (Not macOS)

## The Issue

You're trying to run on macOS, but CocoaPods is required for iOS/macOS. Since this is an **Android app for Play Store**, you should run it on **Android** instead.

---

## Solution: Run on Android Emulator/Device

### Step 1: Check Available Devices

Run this command:
```bash
cd /Users/akshay/Desktop/Projects/wordcrypt/mobile
flutter devices
```

You should see something like:
```
2 connected devices:

sdk gphone64 arm64 (mobile) • emulator-5554 • android-arm64  • Android 14 (API 34)
macOS (desktop)             • macos         • darwin-arm64  • macOS 15.6
```

### Step 2: Create Android Emulator (If None Available)

1. **Open Android Studio**
2. Go to **Tools** → **Device Manager**
3. Click **Create Device**
4. Select a device (e.g., **Pixel 5**)
5. Click **Next**
6. Select a system image (e.g., **API 34 - Android 14**)
7. Click **Download** if needed, then **Next**
8. Click **Finish**
9. Click **Play** button to start the emulator

### Step 3: Run on Android Device

**Option A: Using Android Studio**

1. **Select Android device** from device dropdown (top toolbar)
   - Should show your emulator or connected device
   - NOT "macOS" or "Chrome"
2. Click **Run** button (green play icon)

**Option B: Using Terminal**

```bash
cd /Users/akshay/Desktop/Projects/wordcrypt/mobile

# List devices
flutter devices

# Run on specific Android device
flutter run -d <android-device-id>

# Example:
flutter run -d emulator-5554
```

---

## Quick Fix: Specify Android Device

If Android Studio keeps defaulting to macOS:

1. **In Android Studio:**
   - Look at the device dropdown (top toolbar, next to Run button)
   - Click the dropdown
   - Select your **Android emulator** or **connected Android device**
   - NOT "macOS" or "macos"

2. **Or use terminal:**
   ```bash
   cd /Users/akshay/Desktop/Projects/wordcrypt/mobile
   flutter run -d android
   ```

---

## If You Need macOS Support (Optional)

If you want to run on macOS for testing (not required for Play Store):

1. **Install CocoaPods:**
   ```bash
   sudo gem install cocoapods
   ```

2. **Navigate to iOS directory:**
   ```bash
   cd /Users/akshay/Desktop/Projects/wordcrypt/mobile/ios
   pod install
   ```

3. **Then run:**
   ```bash
   cd /Users/akshay/Desktop/Projects/wordcrypt/mobile
   flutter run -d macos
   ```

**But for Play Store, you only need Android!**

---

## Recommended: Use Android Emulator

1. **Start Android Emulator:**
   - Open Android Studio
   - Tools → Device Manager
   - Click Play button on your emulator

2. **Wait for emulator to boot** (may take 1-2 minutes)

3. **Run app:**
   ```bash
   cd /Users/akshay/Desktop/Projects/wordcrypt/mobile
   flutter run
   ```
   Flutter will automatically detect and use the Android emulator.

---

## Verify Device Selection

Before running, check:
```bash
flutter devices
```

You should see an Android device listed. If not:
- Start Android emulator, OR
- Connect Android phone with USB debugging enabled

---

## Summary

✅ **For Play Store:** Run on Android (emulator or device)  
❌ **Don't need:** macOS/iOS for Android Play Store deployment  
⚠️ **Current issue:** Running on macOS instead of Android

**Fix:** Select Android device from dropdown in Android Studio, or use `flutter run -d android` in terminal.

