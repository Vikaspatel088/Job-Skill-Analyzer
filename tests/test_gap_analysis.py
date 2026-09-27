"""Tests for candidate comparison and skill gap analysis."""

from __future__ import annotations

import pytest

from job_skill_analyzer.analyzer import JobSkillAnalyzer


@pytest.fixture
def analyzer() -> JobSkillAnalyzer:
    return JobSkillAnalyzer()


def test_gap_analysis_when_no_candidate_skills_provided(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Looking for a Python developer with FastAPI, PostgreSQL, Docker and AWS experience."
    report = analyzer.analyze(job_text, candidate_skills=None)
    comp = report.candidate_comparison
    # Must NOT claim AWS or any skill is missing if candidate skills weren't provided!
    assert comp.provided is False
    assert len(comp.matched_skills) == 0
    assert len(comp.missing_skills) == 0


def test_gap_analysis_everything_matched(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Required skills: Python, Docker, PostgreSQL."
    cand_skills = "Python, Docker, PostgreSQL"
    report = analyzer.analyze(job_text, candidate_skills=cand_skills)
    comp = report.candidate_comparison
    assert comp.provided is True
    assert set(comp.matched_skills) == {"Python", "Docker", "PostgreSQL"}
    assert len(comp.missing_skills) == 0
    assert comp.match_percentage == 100.0


def test_gap_analysis_partially_matched(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Required skills: Python, FastAPI, PostgreSQL, Docker, AWS, REST API."
    cand_skills = "Python, FastAPI, PostgreSQL, Docker, REST API"
    report = analyzer.analyze(job_text, candidate_skills=cand_skills)
    comp = report.candidate_comparison
    assert comp.provided is True
    assert set(comp.matched_skills) == {"Python", "FastAPI", "PostgreSQL", "Docker", "REST API"}
    assert comp.missing_skills == ["AWS"]
    assert round(comp.match_percentage, 1) == 83.3


def test_gap_analysis_everything_missing(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Required skills: Python, AWS, Docker."
    cand_skills = "Java, PHP, Ruby"
    report = analyzer.analyze(job_text, candidate_skills=cand_skills)
    comp = report.candidate_comparison
    assert comp.provided is True
    assert len(comp.matched_skills) == 0
    assert set(comp.missing_skills) == {"Python", "AWS", "Docker"}
    assert comp.match_percentage == 0.0


def test_gap_analysis_normalizes_candidate_aliases(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Required skills: PostgreSQL, JavaScript, Kubernetes, Google Cloud."
    # Candidate uses aliases: postgres, js, k8s, gcp
    cand_skills = "postgres, js, k8s, gcp"
    report = analyzer.analyze(job_text, candidate_skills=cand_skills)
    comp = report.candidate_comparison
    assert comp.provided is True
    assert set(comp.matched_skills) == {"PostgreSQL", "JavaScript", "Kubernetes", "Google Cloud"}
    assert len(comp.missing_skills) == 0
    assert comp.match_percentage == 100.0


def test_gap_analysis_empty_candidate_string_provided(analyzer: JobSkillAnalyzer) -> None:
    job_text = "Required skills: Python, AWS."
    report = analyzer.analyze(job_text, candidate_skills="   ")
    comp = report.candidate_comparison
    assert comp.provided is True
    assert len(comp.matched_skills) == 0
    assert set(comp.missing_skills) == {"Python", "AWS"}
    assert comp.match_percentage == 0.0
