---
name: auth-guard-check
description: 인증이 필요한 화면, 핸들러, mutation, 서비스 호출에서 auth guard 누락을 점검할 때 사용한다. 로그인 필요 액션, user null, 401/403, entitlement, 결제, 업로드, 생성 작업에 적용한다.
---

# Auth Guard Check

## Checklist

- Identify actions that require a signed-in user: create, update, delete, upload, purchase, subscribe, favorite, bookmark, start chat, view private data.
- Check the nearest UI handler first. It should stop unauthenticated users before side effects begin.
- Check service and mutation layers for `userId` or session assumptions.
- Make unauthenticated behavior explicit: prompt login, return a typed error, or block the action.
- Verify development bypass flags do not leak into production behavior.

## Rules

- Do not rely only on hidden buttons. Protected side effects still need guardrails.
- Keep user-facing messages project-local and product-appropriate.
- If backend authorization is involved, verify the backend policy or API contract separately.

