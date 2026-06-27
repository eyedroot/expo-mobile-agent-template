---
name: zustand-patterns
description: Zustand 스토어 생성, 수정, persist, initialization, selector, service-layer boundary 작업 시 사용한다.
---

# Zustand Patterns

## Store Design

- Keep store state and actions cohesive around one domain.
- Avoid importing one store from another store file. Use services or screen-level orchestration to prevent cyclic initialization.
- Export store-related types from the store file when they are domain-specific.
- Keep storage keys centralized when the project has a `STORAGE_KEYS` constant.

## Persistence

- Use explicit partial persistence instead of saving the entire store by default.
- Track initialization state when persisted data affects app startup.
- Put rehydration handling in the store configuration when possible, not scattered route effects.

## Selectors

- Prefer stable selectors. If project convention uses `useShallow`, follow it consistently.
- Avoid returning fresh objects or arrays from selectors unless shallow comparison is used.

## Verification

- Test cold start, reload, logout/reset, and persisted state migration paths when store shape changes.

