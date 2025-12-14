# Google Play Store Deployment - Quick Checklist

Use this checklist to ensure you complete all steps before submitting your app.

## Pre-Build Checklist

- [ ] Update `pubspec.yaml`:
  - [ ] Change app name from "mobile" to "wordcrypt"
  - [ ] Update description
  - [ ] Set version (1.0.0+1)

- [ ] Update `android/app/build.gradle.kts`:
  - [ ] Change applicationId to "com.wordcrypt.app"
  - [ ] Set minSdk to 21
  - [ ] Set targetSdk to 34
  - [ ] Set versionCode and versionName

- [ ] Update API URL in `lib/services/api_service.dart`:
  - [ ] Change to production backend URL
  - [ ] Ensure HTTPS is enabled

- [ ] Create app icon (512x512 PNG):
  - [ ] Design or source app icon
  - [ ] Generate all densities using Android Studio

## Keystore Setup

- [ ] Generate keystore file:
  ```bash
  keytool -genkey -v -keystore wordcrypt-keystore.jks \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -alias wordcrypt
  ```

- [ ] Create `android/key.properties`:
  - [ ] Copy from `key.properties.example`
  - [ ] Fill in passwords and paths
  - [ ] Verify file is in `.gitignore`

- [ ] Update `android/app/build.gradle.kts`:
  - [ ] Add keystore loading code
  - [ ] Configure signing configs
  - [ ] Set release build to use signing config

## Build & Test

- [ ] Clean build:
  ```bash
  flutter clean
  flutter pub get
  ```

- [ ] Build release APK for testing:
  ```bash
  flutter build apk --release
  ```

- [ ] Test release APK:
  - [ ] Install on physical device
  - [ ] Test all game features
  - [ ] Test API connectivity
  - [ ] Test theme toggle
  - [ ] Test statistics
  - [ ] Verify no crashes

- [ ] Build release bundle:
  ```bash
  flutter build appbundle --release
  ```

- [ ] Verify bundle location:
  - [ ] File: `build/app/outputs/bundle/release/app-release.aab`
  - [ ] File size is reasonable (< 50MB)

## Play Store Assets

- [ ] App Icon:
  - [ ] 512x512 PNG
  - [ ] No transparency
  - [ ] High quality

- [ ] Feature Graphic:
  - [ ] 1024x500 PNG
  - [ ] Shows app features
  - [ ] Eye-catching design

- [ ] Screenshots (minimum 2, recommended 4-8):
  - [ ] Main game screen
  - [ ] Statistics screen
  - [ ] Dark mode view
  - [ ] Game over screen
  - [ ] Phone screenshots (16:9 or 9:16)
  - [ ] Tablet screenshots (optional)

- [ ] Store Listing Text:
  - [ ] App name: "WordCrypt"
  - [ ] Short description (80 chars max)
  - [ ] Full description (4000 chars max)
  - [ ] Category: Games → Word

## Play Console Setup

- [ ] Create app in Play Console:
  - [ ] App name: WordCrypt
  - [ ] Default language: English
  - [ ] App or Game: Game
  - [ ] Free or Paid: Free

- [ ] Complete Required Policies:
  - [ ] Privacy Policy URL added
  - [ ] Content Rating completed
  - [ ] Data Safety form completed
  - [ ] Target audience selected

- [ ] Upload App Bundle:
  - [ ] Upload `app-release.aab`
  - [ ] Add release notes
  - [ ] Review release details

- [ ] Complete Store Listing:
  - [ ] All required fields filled
  - [ ] Graphics uploaded
  - [ ] Screenshots uploaded
  - [ ] Description complete

- [ ] Pricing & Distribution:
  - [ ] Set to Free
  - [ ] Select countries (or all)

## Pre-Submission

- [ ] Final Testing:
  - [ ] Test on multiple Android versions
  - [ ] Test on different screen sizes
  - [ ] Verify backend is stable
  - [ ] Check for any console errors

- [ ] Documentation:
  - [ ] Privacy policy is live and accessible
  - [ ] Support email configured (if applicable)

- [ ] Review:
  - [ ] All checkboxes above are checked
  - [ ] No warnings in Play Console
  - [ ] App bundle is valid

## Submit for Review

- [ ] Go to Production → Review release
- [ ] Click "Start rollout to Production"
- [ ] Confirm submission
- [ ] Wait for review (1-3 days typically)

## Post-Submission

- [ ] Monitor Play Console:
  - [ ] Check for review status updates
  - [ ] Respond to any review questions
  - [ ] Address any rejection reasons (if applicable)

- [ ] After Approval:
  - [ ] Share app link
  - [ ] Monitor reviews
  - [ ] Track installs
  - [ ] Respond to user feedback

---

## Quick Command Reference

```bash
# Navigate to mobile directory
cd mobile

# Clean and prepare
flutter clean
flutter pub get

# Build release bundle
flutter build appbundle --release

# Build release APK (for testing)
flutter build apk --release

# Install APK on connected device
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

## Important Reminders

⚠️ **Never commit:**
- `key.properties` file
- `.jks` or `.keystore` files
- Passwords or secrets

✅ **Always:**
- Test release builds before uploading
- Keep keystore file secure and backed up
- Increment versionCode for each release
- Update release notes

---

**Status:** [ ] Not Started | [ ] In Progress | [ ] Ready to Submit | [ ] Submitted | [ ] Published

