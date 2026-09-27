"""Tests for boundary conditions, edge cases, and error handling."""

from __future__ import annotations

import pytest

from job_skill_analyzer.analyzer import JobSkillAnalyzer


@pytest.fixture
def analyzer() -> JobSkillAnalyzer:
    return JobSkillAnalyzer()


def test_empty_job_description_raises_value_error(analyzer: JobSkillAnalyzer) -> None:
    with pytest.raises(ValueError, match="Job description cannot be empty"):
        analyzer.analyze("")


def test_whitespace_only_job_description_raises_value_error(analyzer: JobSkillAnalyzer) -> None:
    with pytest.raises(ValueError, match="Job description cannot be empty"):
        analyzer.analyze("   \n\t  \r\n  ")


def test_no_recognized_skills_found(analyzer: JobSkillAnalyzer) -> None:
    text = "We are hiring for an office administrator to manage front desk operations."
    report = analyzer.analyze(text)
    assert report.total_skills == 0
    assert len(report.skills) == 0
    assert len(report.category_counts) == 0
    assert len(report.priorities) == 0


def test_punctuation_heavy_input(analyzer: JobSkillAnalyzer) -> None:
    text = "!!!---*** [Python] / {FastAPI} ... (PostgreSQL) ? Docker! AWS: -> <REST API> ---###"
    report = analyzer.analyze(text)
    names = {s.name for s in report.skills}
    assert {"Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API"}.issubset(names)


def test_very_long_description_stability(analyzer: JobSkillAnalyzer) -> None:
    # Construct a 2000-word realistic document with scattered skills
    paragraph = (
        "In our enterprise environment, engineers leverage Python and Docker to orchestrate "
        "scalable microservices. Continuous deployment is managed via GitHub Actions and Kubernetes. "
        "Data persistence relies on PostgreSQL and Redis clusters in AWS. "
    )
    long_text = paragraph * 40  # ~1600 words
    report = analyzer.analyze(long_text)
    assert report.total_skills > 0
    # Verify frequencies scaled properly
    skills = {s.name: s for s in report.skills}
    assert skills["Python"].frequency == 40
    assert skills["Docker"].frequency == 40


def test_serialization_to_dict_and_json(analyzer: JobSkillAnalyzer) -> None:
    text = "Requirements: Python, AWS, Docker."
    report = analyzer.analyze(text, candidate_skills="Python")
    report_dict = report.to_dict()
    assert report_dict["total_skills"] == 3
    assert "candidate_comparison" in report_dict
    assert report_dict["candidate_comparison"]["provided"] is True

    json_str = report.to_json()
    assert isinstance(json_str, str)
    assert '"total_skills": 3' in json_str
