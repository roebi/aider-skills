"""
Skill discovery and SKILL.md frontmatter parsing.
Wraps skills-ref where possible, falls back to direct parsing.
"""

from __future__ import annotations

from collections.abc import Iterator  # stdlib (collections)
from dataclasses import dataclass  # stdlib
from pathlib import Path  # stdlib

import yaml  # third-party


@dataclass
class SkillMeta:
    name: str
    description: str
    path: Path
    skill_md: Path

    @property
    def location(self) -> str:
        return str(self.skill_md.resolve())


def _parse_frontmatter(skill_md: Path) -> dict:
    """Extract YAML frontmatter from a SKILL.md file."""
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        return {}


def _is_valid_skill(path: Path) -> bool:
    """A skill is a directory containing a SKILL.md file."""
    return path.is_dir() and (path / "SKILL.md").is_file()


def discover_skills(skills_dirs: list[str | Path]) -> list[SkillMeta]:
    """
    Scan one or more directories for valid skill folders.
    Returns a list of SkillMeta, sorted by name.

    A valid skill folder contains a SKILL.md with name + description
    in its YAML frontmatter.
    """
    skills: list[SkillMeta] = []
    seen: set[Path] = set()

    for raw_dir in skills_dirs:
        base = Path(raw_dir).expanduser().resolve()
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir()):
            if not _is_valid_skill(entry):
                continue
            resolved = entry.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)

            skill_md = entry / "SKILL.md"
            meta = _parse_frontmatter(skill_md)
            name = meta.get("name") or entry.name
            description = meta.get("description") or ""

            skills.append(
                SkillMeta(
                    name=name,
                    description=description,
                    path=entry,
                    skill_md=skill_md,
                )
            )

    return sorted(skills, key=lambda s: s.name)


def iter_skills(skills_dirs: list[str | Path]) -> Iterator[SkillMeta]:
    """Generator version of discover_skills."""
    yield from discover_skills(skills_dirs)
