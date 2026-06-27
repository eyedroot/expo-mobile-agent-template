---
name: update-expo-deps
description: Expo SDK 호환 의존성 및 npm 최신 버전을 점검하고 안전하게 업데이트할 때 사용한다. Expo SDK 업그레이드, expo install --check 결과 처리, 의존성 업데이트 요청에 적용한다.
---

# Update Expo Dependencies

## Workflow

1. Read `package.json`, lockfile type, Expo SDK version, and package manager.
2. Run the project-compatible check, usually `npx expo install --check`.
3. For non-Expo-managed packages, check current npm versions only when the user asked for latest updates.
4. Split candidates into Expo-managed fixes, regular patch/minor updates, and major updates.
5. Ask before broad or major updates unless the user already requested them.
6. Use `npx expo install <packages>` for Expo-managed packages.
7. Rerun `npx expo install --check`, type check, and lint when available.

## Guardrails

- Expo compatibility wins over raw npm latest for Expo-managed native packages.
- Do not edit native project files just to satisfy dependency metadata.
- If the update changes native code requirements, report the need for dev-client rebuild or store build.

