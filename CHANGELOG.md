# Changelog

All notable changes to `aider-skills` will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-02-24

### Added

- `to-prompt` command: generate `<available_skills>` XML for use with aider `/run`
- `to-conventions` command: generate markdown block for `CONVENTIONS.md`,
  with optional `--append FILE` to write directly to a file
- `tmpfile` command: write rendered skills to a temp file and print its path,
  for use with `aider --read $(aider-skills tmpfile ./my-skills)`
- `list` command: human-readable listing of all discovered skills
- `validate` command: validate a single skill directory for spec compliance
- Skill discovery by scanning directories for folders containing `SKILL.md`
- YAML frontmatter parsing following the [agentskills.io](https://agentskills.io) spec
- Fallback to directory name when `name` field is absent from frontmatter
- Support for multiple skill directories in a single invocation
- Automatic deduplication when the same skill path appears more than once
- XML output with `<available_skills>` format optimised for Claude-based models
- `--no-location` flag on `to-prompt` for tool-based agents without filesystem access
- `--format` flag on `tmpfile` to choose between `xml` and `md` output
- Devcontainer support: Podman + GitHub Codespaces compatible,
  named subfolder `.devcontainer/maintainer/` to allow forks their own config
- GitHub Actions CI workflow: tests on Python 3.10, 3.11, 3.12
- GitHub Actions publish workflow: automated PyPI release on git tag via
  PyPI Trusted Publishing (no API token secret required)

### Dependencies

- `click >= 8.0`
- `pyyaml >= 6.0`
