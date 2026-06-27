---
name: routing-patterns
description: Expo Router 라우팅, navigation, modal presentation, header 설정, route constants 작업 시 사용한다.
---

# Routing Patterns

## Route Rules

- Prefer route constants or helper functions when the project has them.
- Keep route file names aligned with Expo Router conventions.
- Centralize common stack screen options in `src/app/_layout.tsx`.
- Avoid declaring stack options in many route files unless the screen genuinely owns unique options.

## Modal Safety

- Guard modal `push`, `replace`, `dismiss`, and `back` actions against repeated taps or overlapping transitions.
- If the project has a navigation lock utility, use it for modal presentation and dismissal.
- When dismissing a modal and immediately pushing another route, wait for the dismiss transition to finish.

## Verification

- For navigation changes, run type check and manually exercise the changed route on iOS or Android when feasible.
- Check deep links if the route is externally addressable.

