"""
Render discovered skills into formats consumable by aider:
  - XML prompt block  (for /run and --read)
  - Conventions text  (for CONVENTIONS.md / --read)
  - Temp file path    (for aider --read $(aider-skills tmpfile ...))
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from .discover import SkillMeta

# ---------------------------------------------------------------------------
# XML format  (matches agentskills.io spec, Claude-optimised)
# ---------------------------------------------------------------------------


def to_xml(skills: list[SkillMeta], *, include_location: bool = True) -> str:
    """
    Render skills as an <available_skills> XML block.
    This is the format expected by Claude-based models per the agentskills spec.

    When include_location=True (default for filesystem-based agents like aider),
    the model can activate a skill by reading the SKILL.md file directly.
    """
    if not skills:
        return "<!-- aider-skills: no skills found -->"

    lines = ["<available_skills>"]
    for skill in skills:
        lines.append("  <skill>")
        lines.append(f"    <name>{_esc(skill.name)}</name>")
        lines.append(f"    <description>{_esc(skill.description)}</description>")
        if include_location:
            lines.append(f"    <location>{_esc(skill.location)}</location>")
        lines.append("  </skill>")
    lines.append("</available_skills>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Conventions format  (plain text, for CONVENTIONS.md injection)
# ---------------------------------------------------------------------------


def to_conventions(skills: list[SkillMeta]) -> str:
    """
    Render skills as a plain-text block suitable for appending to
    aider's CONVENTIONS.md (or any --read file).
    """
    if not skills:
        return ""

    lines = [
        "## Available Agent Skills",
        "",
        "The following skills are available. Read the SKILL.md at each location",
        "before attempting tasks in that domain.",
        "",
    ]
    for skill in skills:
        lines.append(f"### {skill.name}")
        if skill.description:
            lines.append(skill.description)
        lines.append(f"Location: {skill.location}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Temp file  (for aider --read $(aider-skills tmpfile ./skills))
# ---------------------------------------------------------------------------


def to_tmpfile(skills: list[SkillMeta], *, fmt: str = "xml") -> Path:
    """
    Write rendered skills to a named temp file and return its path.
    The file persists until the OS cleans up /tmp — long enough for one
    aider session.

    Usage in shell:
        aider --read $(aider-skills tmpfile ./my-skills)
    """
    content = to_xml(skills) if fmt == "xml" else to_conventions(skills)
    suffix = ".xml" if fmt == "xml" else ".md"

    tf = tempfile.NamedTemporaryFile(
        mode="w",
        prefix="aider-skills-",
        suffix=suffix,
        delete=False,
        encoding="utf-8",
    )
    tf.write(content)
    tf.flush()
    tf.close()
    return Path(tf.name)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _esc(text: str) -> str:
    """Minimal XML escaping for skill names and descriptions."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
