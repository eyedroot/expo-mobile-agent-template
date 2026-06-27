---
name: performance-patterns
description: FlashList, Reanimated, memoization, expensive render paths, list performance, animation performance 작업 시 사용한다.
---

# Performance Patterns

## Lists

- Prefer `FlashList` for large or frequently updated lists when installed.
- With FlashList v2, do not add obsolete `estimatedItemSize`.
- Keep `renderItem`, `keyExtractor`, and item callbacks referentially stable when list churn matters.
- Avoid wrapping scrollable lists with pressables that block gestures.

## Reanimated

- Keep animation work on the UI thread when possible.
- For FlashList and Reanimated scroll handlers, verify compatibility with the installed FlashList version.
- Avoid creating shared values inside loops or item renderers unless each item truly owns animation state.

## React

- Memoize expensive derived values and stable dependency arrays.
- Do not add `memo` everywhere by default. Use it where props are stable and render cost is real.

## Verification

- Use simulator/device testing for scroll, animation, and gesture changes.
- For significant regressions, capture profiler or trace evidence rather than relying on visual feel alone.

