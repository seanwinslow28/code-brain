---
name: rn-debug
description: React Native debugging assistant. Diagnoses build failures, red screens, and performance issues systematically.
---

# RN Debug Skill

## Purpose

Systematically debug React Native issues without the usual trial-and-error chaos. Covers iOS, Android, Expo, and bare RN.

## Clarifying Interview

```
RN Debug Setup:

1. **Environment:** Expo | Bare RN | Expo with ejection
2. **Platform:** iOS | Android | Both
3. **RN Version:** (run: npx react-native --version)
4. **Error type:** Build failure | Red screen | Yellow warning | Performance | Crash
5. **When it started:** After update | After new package | Random | Always
6. **Error message:** [paste exact error]
```

## Debug Decision Tree

### Build Failures

```
Build failing?
├── iOS
│   ├── "No bundle URL present" → Metro not running or wrong IP
│   ├── Pod install failed → rm -rf ios/Pods && pod install --repo-update
│   ├── Signing error → Check Xcode signing settings
│   └── Xcode version mismatch → Check .xcode-version or CI config
│
├── Android
│   ├── "SDK location not found" → Create local.properties
│   ├── Gradle sync failed → ./gradlew clean && ./gradlew --refresh-dependencies
│   ├── NDK error → Check ndk.dir in local.properties
│   └── Java version mismatch → Check JAVA_HOME
│
└── Both
    ├── After npm install → Clear caches (see below)
    └── After RN upgrade → Check upgrade helper: react-native-community/upgrade-helper
```

### Nuclear Cache Clear

```bash
# The "turn it off and on again" for React Native
watchman watch-del-all
rm -rf node_modules
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*
npm cache clean --force
npm install

# iOS specific
cd ios && rm -rf Pods Podfile.lock && pod install --repo-update && cd ..

# Android specific
cd android && ./gradlew clean && cd ..

# Start fresh
npx react-native start --reset-cache
```

### Red Screen Errors

| Error Pattern | Likely Cause | Fix |
|--------------|--------------|-----|
| `undefined is not an object` | Accessing property of null | Add null checks or optional chaining |
| `Cannot read property 'X' of undefined` | Component rendered before data ready | Add loading state |
| `Invariant Violation` | React rules broken (hooks, keys) | Check hook order, add unique keys |
| `Native module cannot be null` | Missing native linking | `npx pod-install` or rebuild |
| `Network request failed` | iOS ATS or Android cleartext | Check Info.plist / AndroidManifest |

### Performance Debugging

```typescript
// 1. Enable performance monitor
// Shake device → "Show Perf Monitor"

// 2. Common culprits
// - FlatList without keyExtractor
// - Images without dimensions
// - Inline functions in render
// - Missing React.memo on list items

// 3. Profile with Flipper
// - Install Flipper: https://fbflipper.com
// - Enable React DevTools plugin
// - Check "Highlight Updates" for unnecessary rerenders

// 4. Console.log in production
// Strip logs in production:
if (__DEV__) {
  console.log('debug info');
}
```

### Expo-Specific Issues

```
Expo issues?
├── "Invariant Violation: Native module cannot be null"
│   └── Package needs native code → Create dev build or eject
│
├── EAS Build failing
│   └── Check eas.json profile matches package.json
│
├── OTA update not working
│   └── Check app.json version and runtimeVersion
│
└── SDK version mismatch
    └── npx expo install --check
```

## Success Criteria

- [ ] Error is reproducible (can describe exact steps)
- [ ] Root cause identified (not just symptom)
- [ ] Fix doesn't introduce new issues
- [ ] Similar errors prevented (added error boundary, null checks, etc.)

## Verification Steps

1. **Reproduce:** Can you trigger the error consistently?
2. **Isolate:** Does error occur in minimal reproduction?
3. **Fix:** Does the fix address root cause, not just symptom?
4. **Regression:** Did you test related functionality?

## Context Gathering (Minimal)

Only pull:
- `package.json` - Dependencies and versions
- Error stack trace file (if mentioned)
- Specific component file causing error

**Do NOT pull:** All source files, assets, ios/android folders

## Diagnostic Commands

```bash
# Environment info (include in bug reports)
npx react-native info

# Check for dependency issues
npx react-native doctor

# Expo equivalent
npx expo doctor

# Find duplicate packages
npm ls react-native
npm ls react

# Check native module linking
npx react-native config
```

## Copy/Paste Ready

```
/rn-debug "Cannot read property 'navigate' of undefined"
/rn-debug iOS build failing after pod install
/rn-debug Android app crashes on startup
/rn-debug FlatList performance is terrible
/rn-debug Expo EAS build failing
```
