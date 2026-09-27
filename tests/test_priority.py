"""Tests for deterministic skill priority evaluation."""

from __future__ import annotations

import pytest

from job_skill_analyzer.analyzer import JobSkillAnalyzer
from job_skill_analyzer.models import PriorityLevel


@pytest.fixture
def analyzer() -> JobSkillAnalyzer:
    return JobSkillAnalyzer()


def test_priority_relative_weights(analyzer: JobSkillAnalyzer) -> None:
    # Per specification: AWS -> High, Docker -> Medium, Git -> Low
    job_text = "We need skills in AWS, Docker, and Git."
    report = analyzer.analyze(job_text)
    priorities = {p.skill_name: p for p in report.priorities}

    assert priorities["AWS"].priority == PriorityLevel.HIGH
    assert priorities["Docker"].priority == PriorityLevel.MEDIUM
    assert priorities["Git"].priority == PriorityLevel.LOW

    # Verify explainable reasons are populated
    for p in priorities.values():
        assert p.reason and len(p.reason) > 5


def test_frequency_elevates_to_high_priority(analyzer: JobSkillAnalyzer) -> None:
    # Git is normally LOW as a tool, but repeated mentions elevate its priority
    job_text = "Git proficiency is essential. We use Git daily for version control."
    report = analyzer.analyze(job_text)
    priorities = {p.skill_name: p for p in report.priorities}

    assert priorities["Git"].priority == PriorityLevel.HIGH
    assert "2 mentions" in priorities["Git"].reason


def test_missing_skills_prioritization_for_candidate(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Required skills: Python, AWS, Docker, and Git."
    # Candidate knows Python; lacks AWS (Cloud), Docker (DevOps), Git (Tools)
    cand_skills = "Python"
    report = analyzer.analyze(job_text, candidate_skills=cand_skills)

    missing_priorities = {p.skill_name: p for p in report.priorities if p.is_missing}
    assert missing_priorities["AWS"].priority == PriorityLevel.HIGH
    assert missing_priorities["Docker"].priority == PriorityLevel.MEDIUM
    assert missing_priorities["Git"].priority == PriorityLevel.LOW
