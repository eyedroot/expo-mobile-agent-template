---
name: expo-ui-patterns
description: @expo/ui SwiftUI/Jetpack Compose native components를 추가, 수정, 디버깅할 때 사용한다. Host, Picker, Toggle, Menu, DateTimePicker, platform file split 작업에 적용한다.
---

# @expo/ui Patterns

## Platform Files

`@expo/ui` native views may call native registration at module load time. For shared imports, split platform implementations:

- `Component.ios.tsx`: SwiftUI implementation.
- `Component.android.tsx`: Jetpack Compose implementation.
- `Component.tsx`: safe fallback with the same props, usually `return null`.

## Layout

- Verify `Host` sizing on each platform.
- Be careful with intrinsic native component sizes inside flex layouts.
- Test the actual simulator when layout bugs involve native controls.

## Version Check

- Read the installed `@expo/ui` version from `package.json`.
- Check official Expo docs before using newly introduced components or props.

