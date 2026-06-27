---
name: mobile-simulator-control
description: iOS Simulator 또는 Android Emulator 화면 조작/검증이 필요할 때 사용한다. screenshot, tap, swipe, reload, deep link, UI hierarchy 확인에 적용한다.
---

# Mobile Simulator Control

## Selection

- iOS Simulator: prefer available simulator MCP tools. If unavailable, use `xcrun simctl` for boot/status/screenshot/deeplink and `idb` for taps or swipes.
- Android Emulator: use `adb` for status, screenshot, input, logcat, and deeplink.

## iOS Checklist

```bash
xcrun simctl list devices | grep -i booted
xcrun simctl io booted screenshot /tmp/app-screen.png
```

Use `idb list-targets` before `idb ui tap` or `idb ui swipe`.

## Android Checklist

```bash
adb devices
adb exec-out screencap -p > /tmp/app-screen.png
adb shell input tap 100 100
```

## Rules

- Prefer semantic UI automation tools when available.
- Capture screenshots before and after risky UI interactions.
- Do not assume a simulator is already running; inspect first.
- Include platform, device, and verification result in the final report.

