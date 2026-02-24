# aider-skills

> [Agent Skills](https://agentskills.io) integration for [aider](https://aider.chat) —
> inject structured skills into your AI pair programming sessions with zero aider changes.

[![CI](https://github.com/YOUR_USERNAME/aider-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/aider-skills/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/aider-skills)](https://pypi.org/project/aider-skills/)
[![Python](https://img.shields.io/pypi/pyversions/aider-skills)](https://pypi.org/project/aider-skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Install

```bash
pip install aider-skills
```

## Quickstart

```bash
# Inside an aider session:
/run aider-skills to-prompt ./my-skills

# Or at startup:
aider --read $(aider-skills tmpfile ./my-skills)
```

The model receives structured metadata about available skills and reads
individual `SKILL.md` files on demand — exactly as the
[agentskills.io spec](https://agentskills.io/integrate-skills) describes
for filesystem-based agents.

## Why

Aider has no plugin or hook system. `aider-skills` uses aider's own
`/run` command and `--read` flag as integration points, requiring no
fork and no changes to aider's internals.

## Documentation

See [docs/aider-integration.md](docs/aider-integration.md) for full usage,
all three integration patterns, and skill authoring guidance.

## Commands

| Command | What it does |
|---|---|
| `to-prompt DIR...` | Print `<available_skills>` XML — use with `/run` |
| `to-conventions DIR...` | Print markdown block — use with `CONVENTIONS.md` |
| `tmpfile DIR...` | Write to temp file, print path — use with `--read` |
| `list DIR...` | Human-readable list of discovered skills |
| `validate DIR` | Validate a single skill directory |

## Related

- [agentskills.io](https://agentskills.io) — the Agent Skills specification
- [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) — reference implementation this wraps
- [aider](https://aider.chat) — AI pair programming in your terminal
- [cecli](https://cecli.dev) — aider fork with native skills support built in

## License

MIT
