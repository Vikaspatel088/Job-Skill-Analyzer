"""Tests for skill taxonomy categorization."""

from __future__ import annotations

import pytest

from job_skill_analyzer.extractor import SkillExtractor
from job_skill_analyzer.models import SkillCategory
from job_skill_analyzer.taxonomy import (
    SKILL_DEFINITIONS,
    get_definition_map,
    get_skills_by_category,
)


def test_taxonomy_has_all_required_categories() -> None:
    category_map = get_skills_by_category()
    expected_categories = {
        SkillCategory.PROGRAMMING_LANGUAGE,
        SkillCategory.FRAMEWORK,
        SkillCategory.DATABASE,
        SkillCategory.CLOUD,
        SkillCategory.DEVOPS,
        SkillCategory.API_BACKEND,
        SkillCategory.AI_DATA,
        SkillCategory.TOOLS,
    }
    assert set(category_map.keys()) == expected_categories
    for cat in expected_categories:
        assert len(category_map[cat]) > 0, f"Category {cat.value} has no skills assigned"


@pytest.mark.parametrize(
    "skill_name,expected_category",
    [
        ("Python", SkillCategory.PROGRAMMING_LANGUAGE),
        ("Java", SkillCategory.PROGRAMMING_LANGUAGE),
        ("JavaScript", SkillCategory.PROGRAMMING_LANGUAGE),
        ("C++", SkillCategory.PROGRAMMING_LANGUAGE),
        ("FastAPI", SkillCategory.FRAMEWORK),
        ("React", SkillCategory.FRAMEWORK),
        ("Django", SkillCategory.FRAMEWORK),
        (".NET", SkillCategory.FRAMEWORK),
        ("PostgreSQL", SkillCategory.DATABASE),
        ("MySQL", SkillCategory.DATABASE),
        ("MongoDB", SkillCategory.DATABASE),
        ("AWS", SkillCategory.CLOUD),
        ("Google Cloud", SkillCategory.CLOUD),
        ("Docker", SkillCategory.DEVOPS),
        ("Kubernetes", SkillCategory.DEVOPS),
        ("CI/CD", SkillCategory.DEVOPS),
        ("REST API", SkillCategory.API_BACKEND),
        ("GraphQL", SkillCategory.API_BACKEND),
        ("Microservices", SkillCategory.API_BACKEND),
        ("Machine Learning", SkillCategory.AI_DATA),
        ("Natural Language Processing", SkillCategory.AI_DATA),
        ("Git", SkillCategory.TOOLS),
        ("Linux", SkillCategory.TOOLS),
    ],
)
def test_skill_category_mapping(skill_name: str, expected_category: SkillCategory) -> None:
    def_map = get_definition_map()
    assert skill_name in def_map
    assert def_map[skill_name].category == expected_category


def test_extracted_skill_has_correct_category() -> None:
    extractor = SkillExtractor()
    text = "We use Python, PostgreSQL, Docker, AWS, React, and REST API."
    skills = {s.name: s.category for s in extractor.extract(text)}
    assert skills["Python"] == SkillCategory.PROGRAMMING_LANGUAGE
    assert skills["PostgreSQL"] == SkillCategory.DATABASE
    assert skills["Docker"] == SkillCategory.DEVOPS
    assert skills["AWS"] == SkillCategory.CLOUD
    assert skills["React"] == SkillCategory.FRAMEWORK
    assert skills["REST API"] == SkillCategory.API_BACKEND
