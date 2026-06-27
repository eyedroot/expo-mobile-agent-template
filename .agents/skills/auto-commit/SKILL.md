---
name: auto-commit
description: 현재 git diff를 분석해 커밋 메시지를 제안하고, 사용자 승인 후 git add/commit을 수행할 때 사용한다.
---

# Auto Commit

## Workflow

1. Run `git status --short --branch`, `git diff`, `git diff --cached`, and `git log --oneline -5`.
2. Identify unrelated changes and do not stage them.
3. Check for sensitive files such as `.env`, credentials, tokens, certificates, private keys, and generated secrets.
4. Suggest a concise commit message.
5. Commit only after explicit user approval.

## Message Format

Use `<type>: <subject>` unless the project has a different convention.

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`.

## Signing

If the project requires signed commits, verify signing before committing. Stop instead of creating an unsigned commit when signing is unavailable.

