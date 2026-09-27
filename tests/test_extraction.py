"""Tests for skill extraction engine."""

from __future__ import annotations

import pytest

from job_skill_analyzer.extractor import SkillExtractor


@pytest.fixture
def extractor() -> SkillExtractor:
    return SkillExtractor()


def test_extract_single_skill(extractor: SkillExtractor) -> None:
    text = "We are hiring a Python developer."
    skills = extractor.extract(text)
    assert len(skills) == 1
    assert skills[0].name == "Python"
    assert skills[0].frequency == 1
    assert skills[0].matched_terms == ["Python"]


def test_extract_multiple_skills(extractor: SkillExtractor) -> None:
    text = "Looking for a Python developer with FastAPI, PostgreSQL, Docker and AWS experience."
    skills = extractor.extract(text)
    names = {s.name for s in skills}
    assert names == {"Python", "FastAPI", "PostgreSQL", "Docker", "AWS"}


def test_extract_multi_word_skills(extractor: SkillExtractor) -> None:
    text = (
        "Core competencies include Machine Learning, Deep Learning, "
        "Computer Vision, Natural Language Processing, REST API, "
        "GitHub Actions, and Google Cloud."
    )
    skills = extractor.extract(text)
    names = {s.name for s in skills}
    assert "Machine Learning" in names
    assert "Deep Learning" in names
    assert "Computer Vision" in names
    assert "Natural Language Processing" in names
    assert "REST API" in names
    assert "GitHub Actions" in names
    assert "Google Cloud" in names


def test_extract_repeated_skills_frequency(extractor: SkillExtractor) -> None:
    text = (
        "We love Python. A senior Python engineer will write clean Python code. "
        "Experience with Docker is also required."
    )
    skills = extractor.extract(text)
    skill_dict = {s.name: s for s in skills}
    assert skill_dict["Python"].frequency == 3
    assert skill_dict["Docker"].frequency == 1


def test_extract_mixed_casing(extractor: SkillExtractor) -> None:
    text = "REQUIREMENTS: pYtHoN, dOcKeR, poStgReSQL, faStAPi, aWs."
    skills = extractor.extract(text)
    names = {s.name for s in skills}
    assert names == {"Python", "Docker", "PostgreSQL", "FastAPI", "AWS"}


def test_extract_special_punctuation_skills(extractor: SkillExtractor) -> None:
    text = "Proficiency in C++, C#, .NET, CI/CD, and Node.js is required."
    skills = extractor.extract(text)
    names = {s.name for s in skills}
    assert {"C++", "C#", ".NET", "CI/CD", "Node.js"}.issubset(names)


def test_extract_avoids_substring_false_positives(extractor: SkillExtractor) -> None:
    # "C" should not match in Chicago or Cat
    # "Go" should not match in Django, Good, or Going
    # "Java" should not match in JavaScript
    # "React" should not match in Reaction
    text = "A good engineer in Chicago had a reaction to outgoing Django code."
    skills = extractor.extract(text)
    names = {s.name for s in skills}
    assert "C" not in names
    assert "Go" not in names
    assert "React" not in names
    assert "Django" in names  # Django should match


def test_extract_unknown_skills_returns_empty_or_known_only(extractor: SkillExtractor) -> None:
    text = "Looking for experience in QuantumQuirk and HyperFluxDB."
    skills = extractor.extract(text)
    assert len(skills) == 0


def test_extract_slash_separated_skills(extractor: SkillExtractor) -> None:
    text = "Looking for Python/Django and React/TypeScript expertise."
    skills = extractor.extract(text)
    names = {s.name for s in skills}
    assert {"Python", "Django", "React", "TypeScript"}.issubset(names)
