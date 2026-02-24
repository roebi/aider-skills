# Using aider-skills with aider

`aider-skills` is a standalone CLI tool that injects
[Agent Skills](https://agentskills.io) into [aider](https://aider.chat)
sessions. It requires **zero changes** to aider itself.

## Install

```bash
pip install aider-skills
```

## Three integration patterns

### Pattern 1 — `/run` inside a session (recommended)

The most flexible approach. Inject skills at any point during a session.

Inside aider, type:

```
/run aider-skills to-prompt ./my-skills
```

The XML block is printed to the terminal and automatically added to the
chat context. The model will read individual `SKILL.md` files via `/run`
or direct file reads as it needs them.

You can inject from multiple directories:

```
/run aider-skills to-prompt ~/global-skills ./project-skills
```

---

### Pattern 2 — `--read` at startup (automatic, per project)

Write skills to a temp file and pass it to aider at launch:

```bash
aider --read $(aider-skills tmpfile ./my-skills)
```

The skills are available from the first message. The temp file is
automatically cleaned up by the OS.

For a persistent project-level setup, commit a `skills-context.xml` file:

```bash
aider-skills to-prompt ./my-skills > skills-context.xml
aider --read skills-context.xml
```

---

### Pattern 3 — `CONVENTIONS.md` (always-on, global)

Append skills to your conventions file so they're always injected:

```bash
aider-skills to-conventions ./my-skills --append CONVENTIONS.md
```

Then use aider normally — it reads `CONVENTIONS.md` automatically
if you have `read: CONVENTIONS.md` in `.aider.conf.yml`:

```yaml
# .aider.conf.yml
read:
  - CONVENTIONS.md
```

---

## Creating skills

A skill is a folder containing a `SKILL.md` with YAML frontmatter:

```
my-skills/
└── python-refactoring/
    ├── SKILL.md
    ├── references/
    │   └── patterns.md
    └── scripts/
        └── lint.sh
```

```markdown
---
name: python-refactoring
description: Tools and patterns for refactoring Python code
---

# Python Refactoring

Instructions for the AI go here...
```

Validate your skill:

```bash
aider-skills validate ./my-skills/python-refactoring
```

List all discovered skills:

```bash
aider-skills list ./my-skills
```

---

## All commands

| Command | Description |
|---|---|
| `aider-skills to-prompt DIR...` | Print `<available_skills>` XML (use with `/run`) |
| `aider-skills to-conventions DIR...` | Print markdown block (use with `CONVENTIONS.md`) |
| `aider-skills tmpfile DIR...` | Write to temp file, print path (use with `--read`) |
| `aider-skills list DIR...` | List discovered skills |
| `aider-skills validate DIR` | Validate a single skill directory |

Run `aider-skills --help` or `aider-skills COMMAND --help` for full options.

---

## Skill spec

Skills follow the [agentskills.io specification](https://agentskills.io/specification).
The `<available_skills>` XML format is optimised for Claude-based models.
