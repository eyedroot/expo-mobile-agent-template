# Expo Mobile Agent Instructions

기본 답변은 사용자의 언어와 톤을 따른다. 작업 정확성과 기존 변경사항 보존을 우선한다.

## Scope

This guide is for Expo mobile app projects. Keep app-specific product rules, service names, backend project paths, and deployment details in a short project profile section above these shared rules.

## Working Rules

- Before editing code or files, inspect the relevant files, git status, and existing patterns.
- Do not revert user changes unless explicitly requested.
- Keep changes small and scoped to the requested task.
- Verify uncertain facts from local files, command output, official docs, or web search.
- For current library, SDK, API, platform policy, or Expo behavior, check current official documentation before relying on memory.
- After edits, run the narrowest useful verification command: type check, lint, unit test, Expo check, or simulator validation.
- Do not create commits, pushes, pull requests, releases, or external writes unless the user explicitly asks.

## Expo Runtime Policy

- Do not freeze a new app from this template. Start from `create-expo-app@latest`, then apply these agent files.
- Treat Expo SDK, React, React Native, and Expo Router versions as project-local facts from `package.json`.
- Prefer `npx expo install` or the project's package manager equivalent for Expo-managed packages.
- Use `npx expo install --check` when dependency compatibility is in question.
- Do not assume web support. If the project is mobile-only, avoid web-specific implementation unless requested.

## Tooling Guidance

- Use official Expo docs or Expo MCP for Expo package usage and version-sensitive behavior.
- Use Context7 or official docs for library APIs when available.
- Use simulator automation for mobile UI validation when visual behavior matters.
- Prefer `rg` and `rg --files` for searches.

## Directory Conventions

- `src/app/`: Expo Router routes. Folder structure defines navigation.
- `src/components/`: reusable UI. Put shared primitives under `src/components/ui/`.
- `src/hooks/`: general custom hooks.
- `src/queries/`: React Query hooks named `use*Query.ts` and `use*Mutation.ts`.
- `src/stores/`: Zustand stores named `use*Store`.
- `src/services/`: domain services and side effects.
- `src/utils/` and `src/constants/`: helpers and constants.
- `src/providers/`: app-level providers mounted near the route root.
- `src/@types/`: shared app types and generated service types.
- Prefer the `@/*` alias when it is configured in `tsconfig.json`.

## Planning

- For three or more files, new features, refactors, or cross-module behavior changes, share a short plan before implementation.
- Plans should name the files or areas to change, the data/control flow, and the verification command.
- If new facts change the plan, update it and continue without undoing unrelated user changes.

## Mobile Compatibility

- Mobile users may not update immediately. Keep app code, backend contracts, database migrations, storage paths, and edge functions backward compatible where possible.
- Prefer additive server response changes over breaking shape changes.
- Protect local database migrations with idempotent checks such as column existence tests.

## Git

- Inspect `git status --short --branch` before edits and before final reporting.
- Ignore unrelated dirty files.
- If the project requires signed commits, verify signing setup before committing and stop if signing is unavailable.

## Code Style

- Use TypeScript strictness already configured by the project.
- Early returns use braces: `if (condition) { return; }`.
- Add a blank line between declarations and execution.
- Add a blank line above function `return` statements.
- Keep comments short and useful. Prefer comments that explain intent or non-obvious constraints.
- Avoid unrelated refactors and style churn.

## React Patterns

- Screen components may use `export default function ScreenName()`.
- Reusable components should use `const ComponentName: FC<Props> = (...) =>`.
- Do not define large helper components inline inside route screen files. Move them to `src/components/`.
- Hook order: native/router hooks, third-party hooks, project hooks, React state/memo/ref hooks, store hooks, effects.
- Wrap array/object dependencies created in component bodies with `useMemo` before using them in dependency arrays.
- Use `useState(() => initialValue)` for synchronous one-time initialization when external changes do not need to be tracked.

## UI Rules

- Prefer existing shared UI components before adding new primitives.
- Use a project-level `Container` or equivalent root wrapper for screens to centralize background and safe area behavior.
- Prefer a shared `Touchable`/pressable component for touch behavior.
- Prefer `expo-image`-based shared image components when the project has one; use `contentFit` rather than legacy `resizeMode`.
- Use `FlashList` for large lists when it is installed.
- Keep text within its container across small and large mobile screens.

## Styling

- Follow the project's styling system. If NativeWind is installed, prefer `className` and the local class merge helper.
- Keep colors centralized in `src/constants/colors` or an equivalent token file.
- Do not hardcode brand colors except for official third-party login/payment buttons when required by brand guidelines.
- When using rounded iOS-style surfaces, add `borderCurve: "continuous"` where supported.
- Use `lucide-react-native` for general icons when installed. Use SF Symbols only for iOS-specific affordances.

## Routing

- Use route constants or route helper functions when the project has them.
- Centralize Expo Router stack screen options in `src/app/_layout.tsx` where possible.
- Protect modal presentation/dismissal from double taps or overlapping transitions with a navigation lock or equivalent guard.

## State And Data

- Use React Query for server cache and async fetching.
- Centralize query keys in `src/constants/queryKeys` when the project uses React Query.
- For optimistic mutations, update cache in `onMutate`, roll back in `onError`, and invalidate or reconcile in `onSettled`.
- Keep domain-agnostic pure helpers out of large business files; move them to `src/utils/`.
- In Zustand stores, avoid importing other stores from store files to reduce cyclic initialization risk.
- Use stable selectors such as `useShallow` where the project convention requires it.

## Native Modules

- Libraries that call `requireNativeView()` at module load time should be split into `.ios.tsx` and `.android.tsx` files with a safe `.tsx` fallback if the project imports from shared code.
- Do not add native dependencies without checking Expo SDK compatibility.
- For native build changes, mention whether prebuild or a new dev client is required.

## Security

- Never commit secrets, service role keys, access tokens, refresh tokens, certificates, or private credentials.
- Use environment variables, secure storage, or backend vaults for secrets.
- Do not print secret values in logs or final reports.
- Treat public mobile environment variables as non-secret.

## Skills

Detailed patterns are split into `.agents/skills/*`.

- `zustand-patterns`: Zustand stores, persistence, initialization, service-layer boundaries.
- `routing-patterns`: Expo Router routes, headers, modal navigation, route constants.
- `performance-patterns`: FlashList, Reanimated, memoization, list performance.
- `expo-ui-patterns`: `@expo/ui` native component file splitting and layout issues.
- `build-fix`: collect and fix TypeScript, lint, and Expo build errors.
- `update-expo-deps`: update Expo-compatible dependencies safely.
- `mobile-simulator-control`: inspect and control iOS Simulator or Android Emulator.
- `app-store-preview-assets`: generate localized App Store or Play Store preview screenshots from simulator captures.
- `auth-guard-check`: audit authentication guards for protected actions.
- `ad-patterns`: optional AdMob integration checklist.
- `docs-agent`: maintain AGENTS and skill instructions without overloading shared context.
