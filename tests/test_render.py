"""Tests for render output formats."""

from pathlib import Path

from aider_skills.discover import SkillMeta
from aider_skills.render import to_conventions, to_tmpfile, to_xml


def fake_skill(
    name: str, description: str = "A skill", path: str = "/skills"
) -> SkillMeta:
    p = Path(path) / name
    return SkillMeta(
        name=name,
        description=description,
        path=p,
        skill_md=p / "SKILL.md",
    )


class TestToXml:
    def test_empty_skills(self):
        result = to_xml([])
        assert "no skills found" in result

    def test_contains_skill_name(self):
        result = to_xml([fake_skill("python-refactor")])
        assert "python-refactor" in result

    def test_contains_description(self):
        result = to_xml([fake_skill("s", description="Refactors Python code")])
        assert "Refactors Python code" in result

    def test_contains_location_by_default(self):
        result = to_xml([fake_skill("s")])
        assert "<location>" in result

    def test_no_location_when_disabled(self):
        result = to_xml([fake_skill("s")], include_location=False)
        assert "<location>" not in result

    def test_xml_structure(self):
        result = to_xml([fake_skill("s")])
        assert result.startswith("<available_skills>")
        assert result.strip().endswith("</available_skills>")
        assert "<skill>" in result
        assert "</skill>" in result

    def test_xml_escaping(self):
        result = to_xml([fake_skill("s", description="A & B <test>")])
        assert "&amp;" in result
        assert "&lt;" in result


class TestToConventions:
    def test_empty_skills(self):
        assert to_conventions([]) == ""

    def test_contains_skill_name(self):
        result = to_conventions([fake_skill("my-skill")])
        assert "my-skill" in result

    def test_contains_location(self):
        result = to_conventions([fake_skill("s", path="/my/skills")])
        assert "/my/skills" in result

    def test_has_header(self):
        result = to_conventions([fake_skill("s")])
        assert "Agent Skills" in result


class TestToTmpfile:
    def test_returns_existing_file(self, tmp_path):
        skills = [fake_skill("s")]
        path = to_tmpfile(skills)
        assert path.exists()
        path.unlink()  # cleanup

    def test_xml_format(self):
        skills = [fake_skill("s")]
        path = to_tmpfile(skills, fmt="xml")
        assert path.suffix == ".xml"
        assert "<available_skills>" in path.read_text()
        path.unlink()

    def test_md_format(self):
        skills = [fake_skill("s")]
        path = to_tmpfile(skills, fmt="md")
        assert path.suffix == ".md"
        path.unlink()
