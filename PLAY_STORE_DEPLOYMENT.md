# Google Play Store Deployment Guide

Complete step-by-step guide to deploy WordCrypt mobile app to Google Play Store.

## Prerequisites

✅ You have a Google Play Developer account ($25 one-time fee)
✅ Flutter SDK installed and configured
✅ Android Studio installed
✅ Backend API is deployed and accessible

---

## Step 1: Prepare Your App for Release

### 1.1 Update App Information

**Update `mobile/pubspec.yaml`:**
```yaml
name: wordcrypt  # Change from 'mobile' to 'wordcrypt'
description: "WordCrypt - Daily word puzzle game. Guess the 4-letter word in 8 tries!"
version: 1.0.0+1  # Format: versionName+versionCode
```

**Update `mobile/android/app/build.gradle.kts`:**
```kotlin
defaultConfig {
    applicationId = "com.wordcrypt.app"  // Change to your desired package name
    minSdk = 21  // Minimum Android 5.0 (Lollipop)
    targetSdk = 34  // Latest Android version
    versionCode = 1  // Increment for each release
    versionName = "1.0.0"
}
```

### 1.2 Configure App Icon and Name

**Update `mobile/android/app/src/main/AndroidManifest.xml`:**
```xml
<application
    android:label="WordCrypt"  # Already set
    android:icon="@mipmap/ic_launcher">
```

**Create App Icon:**
- Create a 512x512 PNG icon (required for Play Store)
- Use Android Studio's Image Asset Studio:
  - Right-click `mobile/android/app/src/main/res` → New → Image Asset
  - Select "Launcher Icons"
  - Choose your icon image
  - Generate all densities

### 1.3 Update API URL for Production

**Edit `mobile/lib/services/api_service.dart`:**
```dart
// Change this to your production backend URL
static const String baseUrl = 'https://your-backend-domain.com';
```

**Important:** Make sure your backend:
- Has CORS enabled for mobile apps (if needed)
- Is accessible via HTTPS
- Has a valid SSL certificate

---

## Step 2: Create a Keystore for App Signing

### 2.1 Generate a Keystore

Run this command in your terminal:

```bash
cd /Users/akshay/Desktop/Projects/wordcrypt/mobile/android

keytool -genkey -v -keystore wordcrypt-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias wordcrypt
```

**You'll be prompted for:**
- Keystore password (save this securely!)
- Key password (can be same as keystore password)
- Your name, organization, city, state, country

**Important:** 
- Save the keystore file (`wordcrypt-keystore.jks`) in a secure location
- **NEVER commit this file to Git!**
- Save passwords in a password manager
- You'll need this keystore for ALL future updates

### 2.2 Create Key Properties File

Create `mobile/android/key.properties`:

```properties
storePassword=YOUR_KEYSTORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=wordcrypt
storeFile=../wordcrypt-keystore.jks
```

**Add to `.gitignore`:**
```bash
echo "mobile/android/key.properties" >> mobile/android/.gitignore
echo "mobile/android/*.jks" >> mobile/android/.gitignore
```

### 2.3 Configure Signing in build.gradle.kts

Update `mobile/android/app/build.gradle.kts`:

```kotlin
plugins {
    id("com.android.application")
    id("kotlin-android")
    id("dev.flutter.flutter-gradle-plugin")
}

// Add this at the top level
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    namespace = "com.wordcrypt.app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_11.toString()
    }

    defaultConfig {
        applicationId = "com.wordcrypt.app"
        minSdk = 21
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.release
            minifyEnabled = true
            shrinkResources = true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

flutter {
    source = "../.."
}
```

**Note:** The above uses Groovy syntax. For Kotlin DSL (`.kts`), use:

```kotlin
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    // ... existing config ...
    
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String
        }
    }

    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
        }
    }
}
```

---

## Step 3: Build the Release APK/AAB

### 3.1 Build App Bundle (Recommended for Play Store)

```bash
cd /Users/akshay/Desktop/Projects/wordcrypt/mobile

flutter clean
flutter pub get
flutter build appbundle --release
```

**Output location:** `mobile/build/app/outputs/bundle/release/app-release.aab`

### 3.2 (Optional) Build APK for Testing

```bash
flutter build apk --release
```

**Output location:** `mobile/build/app/outputs/flutter-apk/app-release.apk`

**Test the APK:**
```bash
# Install on connected device
flutter install --release

# Or use adb
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

## Step 4: Prepare Play Store Assets

### 4.1 Required Assets

Create these assets before uploading:

1. **App Icon** (512x512 PNG, no transparency)
2. **Feature Graphic** (1024x500 PNG)
3. **Screenshots** (at least 2, up to 8):
   - Phone: 16:9 or 9:16 ratio, min 320px, max 3840px
   - Tablet: 16:9 or 9:16 ratio
4. **Short Description** (80 characters max)
5. **Full Description** (4000 characters max)

### 4.2 Create Screenshots

Take screenshots of your app:
- Main game screen
- Statistics screen
- Dark mode view
- Game over screen

**Tools:**
- Use Android Studio's Device Manager
- Or use a physical device with screenshot feature
- Or use online tools like AppMockUp

### 4.3 Write Store Listing

**Short Description (80 chars):**
```
Daily word puzzle game. Guess the 4-letter word in 8 tries!
```

**Full Description Template:**
```
🎮 WordCrypt - Daily Word Puzzle Game

Challenge yourself with WordCrypt, a daily word puzzle game that tests your vocabulary and logic skills!

✨ Features:
• Guess the 4-letter word in 8 attempts
• Unique letters only - no duplicates allowed
• Color-coded feedback (green = correct position, yellow = correct letter)
• Track your statistics and win streak
• Beautiful dark and light themes
• Daily new word challenge

🎯 How to Play:
1. Enter a 4-letter word with unique letters
2. Get instant feedback:
   - Green circle = letter in correct position
   - Yellow circle = letter exists but wrong position
   - Grey = letter not in word
3. Use clues to solve the puzzle in 8 tries
4. Track your progress and improve your streak!

📊 Statistics:
• Win percentage
• Current streak
• Guess distribution
• Games played

🌓 Themes:
Switch between light and dark mode for comfortable gameplay anytime.

Play daily and improve your word-solving skills!
```

---

## Step 5: Create App in Google Play Console

### 5.1 Access Play Console

1. Go to [Google Play Console](https://play.google.com/console)
2. Sign in with your developer account
3. Click "Create app"

### 5.2 Fill App Details

**App Name:** WordCrypt

**Default Language:** English (United States)

**App or Game:** Game

**Free or Paid:** Free

**Declarations:**
- ✅ Privacy Policy (required) - Create a privacy policy page
- ✅ Content Rating - Complete questionnaire
- ✅ Target Audience - Select appropriate age group
- ✅ Data Safety - Complete data safety form

---

## Step 6: Upload App Bundle

### 6.1 Create Production Release

1. In Play Console, go to **Production** → **Create new release**
2. Upload your `app-release.aab` file
3. Add **Release notes** (what's new in this version)

**Example Release Notes:**
```
Initial release of WordCrypt!

Features:
- Daily 4-letter word puzzle
- 8 attempts to guess
- Statistics tracking
- Dark/Light theme
- Beautiful, modern UI
```

### 6.2 Review Release

- Check for warnings/errors
- Ensure all required information is filled
- Review app bundle details

---

## Step 7: Complete Store Listing

### 7.1 Main Store Listing

Fill in all required fields:

- **App name:** WordCrypt
- **Short description:** (80 chars max)
- **Full description:** (4000 chars max)
- **App icon:** Upload 512x512 PNG
- **Feature graphic:** Upload 1024x500 PNG
- **Screenshots:** Upload at least 2 screenshots
- **Category:** Games → Word
- **Tags:** word puzzle, word game, daily challenge

### 7.2 Graphics Checklist

- [ ] App icon (512x512, no transparency)
- [ ] Feature graphic (1024x500)
- [ ] Phone screenshots (at least 2)
- [ ] Tablet screenshots (optional but recommended)

---

## Step 8: Complete Required Policies

### 8.1 Privacy Policy

**Required if your app:**
- Collects user data
- Uses internet (your app does - for API calls)

**Create a privacy policy:**
- Use a generator like [Privacy Policy Generator](https://www.privacypolicygenerator.info/)
- Host it on your website or use GitHub Pages
- Add URL in Play Console

**Example Privacy Policy URL:**
```
https://yourdomain.com/privacy-policy
```

### 8.2 Content Rating

1. Go to **Content rating** in Play Console
2. Complete the questionnaire:
   - Does your app contain user-generated content? **No**
   - Does your app contain violence? **No**
   - Does your app contain sexual content? **No**
   - Does your app allow users to communicate? **No**
   - Does your app allow users to share location? **No**
   - Does your app contain ads? **No** (unless you add ads later)
3. Submit for rating (usually instant for simple games)

### 8.3 Data Safety

Complete the Data Safety form:

- **Does your app collect or share user data?** 
  - If you only use local storage: **No**
  - If you send data to your backend: **Yes** (specify what data)

- **Data types collected:**
  - Game statistics (if stored on server)
  - Device ID (if used)

- **Data usage:**
  - App functionality
  - Analytics (if applicable)

---

## Step 9: Set Up Pricing and Distribution

### 9.1 Pricing

- Select **Free** (or set price if paid)
- Select countries for distribution (or select all)

### 9.2 App Access

- **All functionality available without restrictions** (for free games)

---

## Step 10: Review and Publish

### 10.1 Pre-Launch Checklist

- [ ] App bundle uploaded
- [ ] Store listing complete
- [ ] Graphics uploaded (icon, screenshots, feature graphic)
- [ ] Privacy policy added
- [ ] Content rating complete
- [ ] Data safety form complete
- [ ] App tested on multiple devices
- [ ] API URL configured for production
- [ ] Backend is live and accessible

### 10.2 Submit for Review

1. Go to **Production** → **Review release**
2. Click **Start rollout to Production**
3. Confirm submission

**Review Time:**
- Usually 1-3 days for new apps
- Can be longer during busy periods
- You'll receive email notifications

### 10.3 After Approval

- App will be live on Play Store
- Share your app link!
- Monitor reviews and ratings
- Respond to user feedback

---

## Step 11: Post-Launch Maintenance

### 11.1 Update App

For future updates:

1. Increment version in `pubspec.yaml`:
   ```yaml
   version: 1.0.1+2  # versionName+versionCode
   ```

2. Update `build.gradle.kts`:
   ```kotlin
   versionCode = 2
   versionName = "1.0.1"
   ```

3. Build new bundle:
   ```bash
   flutter build appbundle --release
   ```

4. Upload to Play Console → **Production** → **Create new release**

### 11.2 Monitor Performance

- Check Play Console dashboard
- Monitor crash reports
- Review user ratings and reviews
- Track installs and uninstalls

---

## Troubleshooting

### Build Errors

**Error: "key.properties not found"**
- Ensure `key.properties` exists in `mobile/android/`
- Check file paths in the file

**Error: "Keystore file not found"**
- Verify keystore file path in `key.properties`
- Use relative path: `../wordcrypt-keystore.jks`

**Error: "Signing config not found"**
- Check `build.gradle.kts` syntax
- Ensure signing config is in `buildTypes.release`

### Play Console Issues

**App rejected: "Missing Privacy Policy"**
- Add privacy policy URL
- Ensure it's accessible and complete

**App rejected: "Content Rating required"**
- Complete content rating questionnaire
- Wait for rating approval

**Upload failed: "Invalid AAB"**
- Rebuild the app bundle
- Check for build errors
- Ensure signing is configured correctly

---

## Quick Reference Commands

```bash
# Navigate to mobile directory
cd /Users/akshay/Desktop/Projects/wordcrypt/mobile

# Clean build
flutter clean

# Get dependencies
flutter pub get

# Build release bundle
flutter build appbundle --release

# Build release APK (for testing)
flutter build apk --release

# Check app size
flutter build appbundle --release --analyze-size

# Test on device
flutter run --release
```

---

## Important Notes

1. **Keystore Security:**
   - Never share your keystore file
   - Never commit it to Git
   - Store backups securely
   - You'll need it for ALL future updates

2. **Version Numbers:**
   - `versionCode` must increase with each release
   - `versionName` is what users see (can be any format)

3. **Testing:**
   - Always test release builds before uploading
   - Test on multiple Android versions
   - Test with different screen sizes

4. **Backend:**
   - Ensure production backend is stable
   - Monitor API performance
   - Set up error logging

---

## Support Resources

- [Flutter Deployment Guide](https://docs.flutter.dev/deployment/android)
- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [App Bundle Guide](https://developer.android.com/guide/app-bundle)

---

**Good luck with your Play Store launch! 🚀**

