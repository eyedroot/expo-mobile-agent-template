---
name: build-fix
description: TypeScript, Expo build, lint, and dependency compatibility errors를 수집하고 최소 변경으로 수정할 때 사용한다. 사용자가 빌드 에러, 타입 에러, lint 에러 해결을 요청하면 적용한다.
---

# Build Fix

## Workflow

1. Inspect `git status --short --branch` and avoid unrelated changes.
2. Run the narrowest failing command first. Prefer the project's scripts, then fall back to `npx tsc --noEmit`, `npx expo lint`, or `npx expo install --check`.
3. Group errors by blocker type: build, type, lint, dependency compatibility.
4. Read the files directly involved in the first failure group.
5. Apply the smallest coherent fix.
6. Rerun the same command. If a new error appears, repeat from the new first blocker.

## Rules

- Separate compiler build failures, optimization skips, and runtime regressions. Do not rewrite working error handling solely to eliminate a skip.
- Do not silence React Hooks diagnostics globally or add suppression comments just to make lint pass. Confirm analysis limitations before narrowing an exception; lint exceptions do not force compilation.
- For compiler-related failures, use [React Compiler 점검과 호환성](../performance-patterns/references/react-compiler.md) and verify emitted app code as well as runtime behavior.

- Do not refactor unrelated code while fixing build failures.
- Do not downgrade Expo-managed packages unless `expo install --check` or official docs clearly require it.
- If native modules changed, mention whether a prebuild or new dev client is required.
- Final report should include the command that failed, the files changed, and the verification result.

