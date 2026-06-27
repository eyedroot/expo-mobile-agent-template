---
name: gh-issue-workflow
description: GitHub 이슈 번호를 기반으로 작업할 때 사용한다. gh issue, GitHub issue, /gh 형식 요청에 적용한다.
---

# GitHub Issue Workflow

## Inputs

An issue number or URL is required. If missing, ask for it in one short question.

## Workflow

1. Read the issue title, body, comments, labels, and linked PRs using `gh issue view` or available GitHub tools.
2. Inspect the local branch, status, and relevant files.
3. Restate concrete requirements before editing when the issue is broad.
4. Implement the narrowest change that satisfies the issue.
5. Run focused verification.
6. Report changed files, verification, and any unresolved issue requirements.

## Boundaries

- Do not create comments, PRs, commits, or status changes unless the user asks.
- Do not trust issue text over current code; inspect the implementation directly.

