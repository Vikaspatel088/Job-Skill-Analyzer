"""Tests for skill normalization and alias resolution."""

from __future__ import annotations

import pytest

from job_skill_analyzer.extractor import SkillExtractor
from job_skill_analyzer.normalizer import (
    clean_text,
    normalize_skill_name,
    parse_and_normalize_skills,
)


@pytest.mark.parametrize(
    "raw_alias,expected_canonical",
    [
        ("postgres", "PostgreSQL"),
        ("postgresql", "PostgreSQL"),
        ("postgres db", "PostgreSQL"),
        ("postgres database", "PostgreSQL"),
        ("js", "JavaScript"),
        ("javascript", "JavaScript"),
        ("ts", "TypeScript"),
        ("typescript", "TypeScript"),
        ("k8s", "Kubernetes"),
        ("kubernetes", "Kubernetes"),
        ("gcp", "Google Cloud"),
        ("google cloud", "Google Cloud"),
        ("google cloud platform", "Google Cloud"),
        ("sklearn", "scikit-learn"),
        ("scikit learn", "scikit-learn"),
        ("scikit-learn", "scikit-learn"),
        ("node", "Node.js"),
        ("nodejs", "Node.js"),
        ("node.js", "Node.js"),
        ("fastapi", "FastAPI"),
        ("fast api", "FastAPI"),
        ("golang", "Go"),
        ("cpp", "C++"),
        ("csharp", "C#"),
        ("dotnet", ".NET"),
        (".net", ".NET"),
        ("cicd", "CI/CD"),
        ("ci/cd", "CI/CD"),
        ("gh actions", "GitHub Actions"),
        ("github actions", "GitHub Actions"),
        ("nlp", "Natural Language Processing"),
        ("ml", "Machine Learning"),
    ],
)
def test_normalize_skill_name(raw_alias: str, expected_canonical: str) -> None:
    assert normalize_skill_name(raw_alias) == expected_canonical


def test_normalize_unknown_skill_returns_none() -> None:
    assert normalize_skill_name("unknown_framework_xyz") is None
    assert normalize_skill_name("") is None


def test_extraction_normalizes_in_context() -> None:
    extractor = SkillExtractor()
    text = "Experience with JS, Postgres, K8s and GCP."
    extracted = extractor.extract(text)
    names = [s.name for s in extracted]
    assert "JavaScript" in names
    assert "PostgreSQL" in names
    assert "Kubernetes" in names
    assert "Google Cloud" in names


def test_parse_and_normalize_candidate_skills() -> None:
    input_str = "postgres, JS, K8s, Python, custom_internal_tool"
    parsed = parse_and_normalize_skills(input_str)
    assert "PostgreSQL" in parsed
    assert "JavaScript" in parsed
    assert "Kubernetes" in parsed
    assert "Python" in parsed
    assert "custom_internal_tool" in parsed


def test_clean_text_normalizes_unicode_and_whitespace() -> None:
    raw = "Skills:  Python \t\n \u2014 \u201cFastAPI\u201d   and   Docker.  "
    cleaned = clean_text(raw)
    assert "Python - \"FastAPI\" and Docker." in cleaned
