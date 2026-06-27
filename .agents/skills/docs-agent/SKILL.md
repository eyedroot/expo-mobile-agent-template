---
name: docs-agent
description: AGENTS.md, README, and .agents/skills instructions를 분석해 공용 지침 반영, 스킬 분리, 중복 제거, 프로젝트 전용 내용 분리 여부를 판단하고 정리할 때 사용한다.
---

# Docs Agent

## Purpose

Keep shared agent instructions compact and reusable. Move detailed, task-specific procedures into skills, and keep product-specific facts in the project profile section.

## Classification

- Shared instructions: rules every agent should follow on most tasks.
- Skill instructions: workflows needed only for a specific task family.
- Project profile: product name, backend paths, deployment channels, bundle identifiers, service contracts, and team-specific commands.
- Discard: facts easily discovered from code, one-off implementation notes, or stale tool behavior.

## Workflow

1. Inspect current files before editing docs.
2. Identify whether each proposed rule is shared, skill-specific, project-specific, or disposable.
3. Compress shared rules to one or two sentences with a reason.
4. Put long examples or command sequences in a skill.
5. Remove duplicate guidance instead of adding another version.
6. Verify no secrets or private service identifiers were added.

