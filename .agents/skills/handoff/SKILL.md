---
name: handoff
description: 현재 작업 상태를 HANDOFF.md에 정리해 다음 에이전트나 새 세션이 이어받을 수 있게 할 때 사용한다.
---

# Handoff

## Output

Write or update `HANDOFF.md` at the project root.

## Format

```markdown
## Goal
- Current user goal.

## Current State
- What has been inspected or changed.

## Decisions
- Important implementation decisions and why.

## Remaining Work
- Concrete next steps.

## Verification
- Commands already run and results.

## Risks
- Known caveats, blockers, or assumptions.
```

## Rules

- Keep it factual and concise.
- Include exact file paths when they matter.
- Do not include secrets.

