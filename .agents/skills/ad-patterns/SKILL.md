---
name: ad-patterns
description: Google Mobile Ads 또는 유사 광고 SDK 통합, ATT/UMP 동의, Ad Unit ID, frequency cap, SDK initialization 작업 시 사용하는 선택 스킬이다.
---

# Ad Patterns

## Setup Checklist

- Keep ad unit IDs and feature flags in centralized constants.
- Use test ad unit IDs in development builds.
- Initialize consent/UMP and tracking permission before loading personalized ads where required.
- Initialize the ad SDK once near app bootstrap.
- Keep load/show logic in hooks or services, not scattered screen handlers.

## Mobile Safety

- Treat store review and platform policy as version-sensitive. Check official SDK and platform docs before release-facing changes.
- Do not log device identifiers, ad IDs, or consent payloads.
- Use frequency caps for interstitial, rewarded, and app-open ads.

## Verification

- Test no-fill, load error, show error, foreground resume, and unmount paths.
- Confirm production ad unit IDs are not used in local development unless explicitly requested.

