# Skill Layers

Agent Skills form a capability iceberg.
The surface is simple — the depth is vast.

---

## Level 1 — Simple Command Skills

The model reads the skill description and runs a single command directly.
No file reading needed if the description is rich enough.

```markdown
---
name: datetime-format
description: Return current timestamp as YYYYMMDD_HHMMSS
---
When asked for the current time, return it formatted as YYYYMMDD_HHMMSS.
```

The model runs:
```bash
date +"%Y%m%d_%H%M%S"
```

**Rule:** Describe the *what*, not the *how*. A capable model finds the right command for its environment (Linux, PowerShell, Python) by itself.

---

## Level 2 — Cascading / Composed Skills

A high-level skill references other skills by name.
The model reads the high-level skill, then reads each referenced skill on demand.
The cascade is driven by model reasoning — no code required.

```markdown
---
name: create-release-note
description: Create a release note combining timestamp and git log
---
## Workflow
1. Use the `datetime-format` skill to get a current timestamp
2. Use the `git-log-summary` skill to get recent commit messages
3. Combine both into a formatted release note
```

The model pulls in each sub-skill's SKILL.md via the `<location>` path as needed.

---

## Level 3 — Sequential Workflows

Explicit ordered steps in a skill, each building on the previous result.
The model follows the sequence and passes context between steps.

```markdown
---
name: analyse-and-report
description: Analyse a CSV file and produce a markdown report
---
## Steps (execute in order)
1. Read the input CSV and summarise its structure
2. Identify anomalies or outliers in the data
3. Generate a markdown report with findings
4. Save the report as YYYYMMDD_HHMMSS_report.md
```

---

## Level 4 — Parallel Synthesis

Gather independent results from multiple skills, then synthesize them.
Aider runs a single thread — the model handles each part sequentially,
but synthesizes them as if they were gathered in parallel.

```markdown
---
name: project-health-check
description: Summarise project health from multiple independent sources
---
## Approach
Gather independently (order does not matter):
- Run the `test-status` skill
- Run the `lint-status` skill
- Run the `dependency-audit` skill

Then synthesize all results into a single health report.
```

---

## Level 5 — Subagents via `/run aider`

A skill spawns a focused sub-aider process for an isolated subtask.
The outer aider orchestrates. The inner aider executes and returns results.

**No MCP. No protocol. No configuration. Just `/run`.**

MCP was a complex solution (server setup, JSON protocol, special integration code)
that `/run` replaces completely. Everything MCP can do, the Unix shell does simpler:

```bash
/run pip install sometool && sometool do-something
/run curl https://api.example.com/data | jq .
/run nohup long-process.sh &
```

A subagent skill:

```markdown
---
name: subagent-analyser
description: Spawn a focused aider subagent to analyse a file independently
---
## Subagent Workflow
Run an isolated analysis using a sub-aider process:
```bash
aider --no-git \
  --message "analyse this file and return a JSON summary" \
  --read input.txt > output.txt
```
Then read output.txt and continue with the result.
```

Subagents can also carry their own skills:
```bash
aider --no-git \
  --read $(aider-skills tmpfile ./skills) \
  --message "your focused subtask" \
  --read data.csv > result.txt
```

---

## Level 6 — Self-Generating Skills

Skills that write new skills.
The system becomes self-improving.

Inspired by [skill-container](https://github.com/observerw/skill-container) —
a skill whose purpose is to generate other properly structured skills
from informal descriptions.

```markdown
---
name: skill-generator
description: Generate a new SKILL.md from an informal task description
---
## Workflow
Given an informal description of a task:
1. Analyse what the skill needs to accomplish
2. Identify required commands, references, and assets
3. Generate a valid SKILL.md with proper YAML frontmatter
4. Validate it with: `aider-skills validate ./skills/<new-skill-name>`
5. Report the new skill location for immediate use
```

A weak description like:
```
"I want a skill that formats dates nicely"
```
becomes a fully structured, validated SKILL.md ready for use.

---

## The Foundation

All levels rest on one primitive:

```
/run = the universal tool
```

The shell is the plugin system.
Unix pipes, background processes, HTTP calls, package installation,
file generation, spawning subagents — all of it, already there,
no integration code required.

```
Level 1  simple command skills         ← start here
Level 2  cascading / composed skills   ← model-driven, no code needed
Level 3  sequential workflows          ← explicit steps in SKILL.md
Level 4  parallel synthesis            ← gather then synthesize
Level 5  subagents via /run aider      ← aider calling aider
Level 6  self-generating skills        ← skills that write skills
```

The `<location>` tag in the injected XML is what makes all levels possible —
it gives the model a path to pull in any skill at any level of the cascade,
on demand, only when needed.
