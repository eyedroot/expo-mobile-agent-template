---
name: performance-patterns
description: React Compiler 적용 여부·Babel 구성·호환성 검증과 FlashList, Reanimated, 메모이제이션, 렌더링 성능 개선 작업 시 사용한다.
---

# Performance Patterns

## Lists

- Prefer `FlashList` for large or frequently updated lists when installed.
- With FlashList v2, do not add obsolete `estimatedItemSize`.
- Keep `renderItem`, `keyExtractor`, and item callbacks referentially stable when list churn matters.
- Avoid wrapping scrollable lists with pressables that block gestures.

## Reanimated

- Keep animation work on the UI thread when possible.
- With React Compiler and a compatible Reanimated version, use SharedValue `get()`/`set()` inside callbacks or Effects, never during render.
- For FlashList and Reanimated scroll handlers, verify compatibility with the installed FlashList version.
- Avoid creating shared values inside loops or item renderers unless each item truly owns animation state.

## React

- Check compiler coverage and measured render cost before adding manual memoization; preserve existing memoization unless its consumers and behavior have been checked.
- Do not add `memo` everywhere by default. Use it where props are stable and render cost is real.

## React Compiler

- For compiler configuration, exclusions, memoization regressions, or related dependency updates, read [React Compiler 점검과 호환성](references/react-compiler.md).
- Verify configuration, emitted app code, and runtime behavior separately; healthcheck or a successful build alone does not establish optimization coverage.

## Verification

- Use simulator/device testing for scroll, animation, and gesture changes.
- For significant regressions, capture profiler or trace evidence rather than relying on visual feel alone.

