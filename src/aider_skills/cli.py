"""
aider-skills CLI

Commands:
  to-prompt       Print <available_skills> XML — use with aider /run
  to-conventions  Print markdown block — append to CONVENTIONS.md
  tmpfile         Write to temp file, print path — use with aider --read
  list            List discovered skills (human-readable)
  validate        Validate a single skill directory
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from .discover import discover_skills
from .render import to_conventions, to_tmpfile, to_xml


# ---------------------------------------------------------------------------
# CLI root
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(package_name="aider-skills")
def main() -> None:
    """
    Agent Skills integration for aider.

    Inject skills into your aider session via /run, --read, or CONVENTIONS.md.

    Quickstart inside aider:

    \b
        /run aider-skills to-prompt ./my-skills
    """


# ---------------------------------------------------------------------------
# to-prompt
# ---------------------------------------------------------------------------

@main.command("to-prompt")
@click.argument("skills_dirs", nargs=-1, required=True, metavar="SKILLS_DIR...")
@click.option(
    "--no-location",
    is_flag=True,
    default=False,
    help="Omit <location> tags (for tool-based agents without filesystem access).",
)
def to_prompt(skills_dirs: tuple[str, ...], no_location: bool) -> None:
    """
    Print <available_skills> XML block to stdout.

    Use inside aider with:

    \b
        /run aider-skills to-prompt ./my-skills
        /run aider-skills to-prompt ~/global-skills ./project-skills

    The output is automatically added to the chat context.
    The model will read individual SKILL.md files as needed.
    """
    skills = discover_skills(list(skills_dirs))
    if not skills:
        click.echo(f"No skills found in: {', '.join(skills_dirs)}", err=True)
        sys.exit(1)
    click.echo(to_xml(skills, include_location=not no_location))


# ---------------------------------------------------------------------------
# to-conventions
# ---------------------------------------------------------------------------

@main.command("to-conventions")
@click.argument("skills_dirs", nargs=-1, required=True, metavar="SKILLS_DIR...")
@click.option(
    "--append",
    "conventions_file",
    default=None,
    metavar="FILE",
    help="Append directly to a file (e.g. CONVENTIONS.md) instead of stdout.",
)
def to_conventions_cmd(
    skills_dirs: tuple[str, ...], conventions_file: str | None) -> None
) -> None:
    """
    Print a markdown skills block suitable for CONVENTIONS.md.

    Use to permanently inject skills at startup:

    \b
        aider-skills to-conventions ./my-skills --append CONVENTIONS.md
        aider --read CONVENTIONS.md

    Or inject once at session start:

    \b
        aider-skills to-conventions ./my-skills >> CONVENTIONS.md
    """
    skills = discover_skills(list(skills_dirs))
    if not skills:
        click.echo(f"No skills found in: {', '.join(skills_dirs)}", err=True)
        sys.exit(1)

    content = to_conventions(skills)

    if conventions_file:
        dest = Path(conventions_file)
        with dest.open("a", encoding="utf-8") as f:
            f.write("\n\n" + content)
        click.echo(f"Appended {len(skills)} skill(s) to {dest}", err=True)
    else:
        click.echo(content)


# ---------------------------------------------------------------------------
# tmpfile
# ---------------------------------------------------------------------------

@main.command("tmpfile")
@click.argument("skills_dirs", nargs=-1, required=True, metavar="SKILLS_DIR...")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["xml", "md"]),
    default="xml",
    show_default=True,
    help="Output format.",
)
def tmpfile_cmd(skills_dirs: tuple[str, ...], fmt: str) -> None:
    """
    Write skills to a temp file and print its path.

    Use with aider --read for automatic startup injection:

    \b
        aider --read $(aider-skills tmpfile ./my-skills)

    The file persists for the duration of your shell session.
    """
    skills = discover_skills(list(skills_dirs))
    if not skills:
        click.echo(f"No skills found in: {', '.join(skills_dirs)}", err=True)
        sys.exit(1)

    path = to_tmpfile(skills, fmt=fmt)
    # Print ONLY the path — so $() substitution works cleanly
    click.echo(str(path))


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

@main.command("list")
@click.argument("skills_dirs", nargs=-1, required=True, metavar="SKILLS_DIR...")
def list_cmd(skills_dirs: tuple[str, ...]) -> None:
    """
    List all discovered skills in human-readable form.

    \b
        aider-skills list ./my-skills
    """
    skills = discover_skills(list(skills_dirs))
    if not skills:
        click.echo(f"No skills found in: {', '.join(skills_dirs)}")
        return

    click.echo(f"Found {len(skills)} skill(s):\n")
    for skill in skills:
        click.echo(f"  {click.style(skill.name, bold=True)}")
        if skill.description:
            click.echo(f"    {skill.description}")
        click.echo(f"    {click.style(skill.location, dim=True)}")
        click.echo()


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------

@main.command("validate")
@click.argument("skill_dir", metavar="SKILL_DIR")
def validate_cmd(skill_dir: str) -> None:
    """
    Validate a single skill directory.

    Checks for SKILL.md presence and required frontmatter fields.

    \b
        aider-skills validate ./my-skills/my-python-skill
    """
    path = Path(skill_dir).expanduser().resolve()
    errors: list[str] = []

    if not path.is_dir():
        click.echo(f"ERROR: Not a directory: {path}", err=True)
        sys.exit(1)

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    else:
        import yaml
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            errors.append("SKILL.md has no YAML frontmatter (expected --- block)")
        else:
            end = content.find("---", 3)
            if end == -1:
                errors.append("SKILL.md frontmatter is not closed with ---")
            else:
                try:
                    meta = yaml.safe_load(content[3:end]) or {}
                    if not meta.get("name"):
                        errors.append("Frontmatter missing required field: name")
                    if not meta.get("description"):
                        errors.append("Frontmatter missing required field: description")
                except yaml.YAMLError as e:
                    errors.append(f"Invalid YAML frontmatter: {e}")

    if errors:
        click.echo(f"INVALID: {path.name}")
        for err in errors:
            click.echo(f"  ✗ {err}")
        sys.exit(1)
    else:
        click.echo(f"✓ Valid skill: {path.name}")
