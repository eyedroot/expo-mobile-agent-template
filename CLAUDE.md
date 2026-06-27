@AGENTS.md

## Claude Code

- This file intentionally imports `AGENTS.md` so Claude Code and other agent tools share the same project instructions without duplicated maintenance.
- Project-specific Claude Code settings live in `.claude/settings.json`.
- Project skills are mirrored into `.claude/skills/` by `scripts/apply-agent-kit.mjs`.
- Keep personal Claude Code preferences in `~/.claude/settings.json` or `.claude/settings.local.json`, not in this shared template.

