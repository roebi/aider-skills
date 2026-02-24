"""Tests for skill discovery and frontmatter parsing."""

from pathlib import Path

from aider_skills.discover import discover_skills


def make_skill(tmp_path: Path, name: str, description: str = "A test skill") -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
    )
    return skill_dir


def test_discovers_valid_skill(tmp_path):
    make_skill(tmp_path, "my-skill", "Does something useful")
    skills = discover_skills([tmp_path])
    assert len(skills) == 1
    assert skills[0].name == "my-skill"
    assert skills[0].description == "Does something useful"


def test_discovers_multiple_skills(tmp_path):
    make_skill(tmp_path, "alpha")
    make_skill(tmp_path, "beta")
    make_skill(tmp_path, "gamma")
    skills = discover_skills([tmp_path])
    assert len(skills) == 3
    # Should be sorted by name
    assert [s.name for s in skills] == ["alpha", "beta", "gamma"]


def test_ignores_dirs_without_skill_md(tmp_path):
    (tmp_path / "not-a-skill").mkdir()
    make_skill(tmp_path, "real-skill")
    skills = discover_skills([tmp_path])
    assert len(skills) == 1


def test_ignores_nonexistent_dir():
    skills = discover_skills(["/this/does/not/exist"])
    assert skills == []


def test_multiple_dirs_deduplication(tmp_path):
    make_skill(tmp_path, "shared-skill")
    # Pass same dir twice — should not duplicate
    skills = discover_skills([tmp_path, tmp_path])
    assert len(skills) == 1


def test_skill_md_path_is_absolute(tmp_path):
    make_skill(tmp_path, "abs-skill")
    skills = discover_skills([tmp_path])
    assert skills[0].skill_md.is_absolute()


def test_fallback_name_from_dirname(tmp_path):
    """If frontmatter has no name, fall back to directory name."""
    skill_dir = tmp_path / "fallback-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\ndescription: No name field\n---\n")
    skills = discover_skills([tmp_path])
    assert skills[0].name == "fallback-skill"
