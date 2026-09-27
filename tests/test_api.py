"""Tests for FastAPI REST API endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from job_skill_analyzer.api import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_sample_endpoint(client: TestClient) -> None:
    response = client.get("/api/sample")
    assert response.status_code == 200
    data = response.json()
    assert "job_description" in data
    assert "candidate_skills" in data
    assert "Python" in data["job_description"]


def test_analyze_endpoint_success(client: TestClient) -> None:
    payload = {
        "job_description": "We need a Python developer with FastAPI, PostgreSQL, Docker, and AWS.",
        "candidate_skills": "Python, Docker, PostgreSQL",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["total_skills"] == 5
    names = {s["name"] for s in data["skills"]}
    assert names == {"Python", "FastAPI", "PostgreSQL", "Docker", "AWS"}
    assert data["candidate_comparison"]["provided"] is True
    assert set(data["candidate_comparison"]["matched_skills"]) == {"Python", "Docker", "PostgreSQL"}
    assert set(data["candidate_comparison"]["missing_skills"]) == {"FastAPI", "AWS"}


def test_analyze_endpoint_core_scenario(client: TestClient) -> None:
    response = client.post(
        "/api/analyze",
        json={
            "job_description": (
                "Looking for a Python developer with FastAPI, PostgreSQL, Docker, AWS and REST API experience. "
                "The candidate should understand Git, CI/CD and microservices."
            ),
            "candidate_skills": "Python, FastAPI, PostgreSQL, Docker, REST API, Git",
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert {skill["name"] for skill in data["skills"]} == {
        "Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API", "Git", "CI/CD", "Microservices"
    }
    comparison = data["candidate_comparison"]
    assert len(comparison["matched_skills"]) == 6
    assert set(comparison["missing_skills"]) == {"AWS", "CI/CD", "Microservices"}
    assert comparison["match_percentage"] == 66.7


def test_analyze_endpoint_does_not_expose_internal_errors(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_analysis(**kwargs: object) -> None:
        raise RuntimeError("internal detail")

    monkeypatch.setattr("job_skill_analyzer.api.analyzer.analyze", fail_analysis)
    response = client.post("/api/analyze", json={"job_description": "Python"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Analysis failed. Please try again."
    assert "internal detail" not in response.text


def test_analyze_endpoint_no_candidate_skills(client: TestClient) -> None:
    payload = {
        "job_description": "Experience with JavaScript and React required.",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_skills"] == 2
    assert data["candidate_comparison"]["provided"] is False
    assert len(data["candidate_comparison"]["matched_skills"]) == 0
    assert len(data["candidate_comparison"]["missing_skills"]) == 0


def test_analyze_endpoint_empty_input_rejected(client: TestClient) -> None:
    response = client.post("/api/analyze", json={"job_description": "   "})
    assert response.status_code == 422


def test_html_report_endpoint(client: TestClient) -> None:
    payload = {
        "job_description": "Looking for Go and Kubernetes engineer.",
        "candidate_skills": "Go",
    }
    response = client.post("/api/report/html", json=payload)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "--color-deep-navy: #14252C" in response.text
    assert "Kubernetes" in response.text


def test_html_report_endpoint_hides_internal_errors(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_analysis(**kwargs: object) -> None:
        raise RuntimeError("internal detail")

    monkeypatch.setattr("job_skill_analyzer.api.analyzer.analyze", fail_analysis)
    response = client.post("/api/report/html", json={"job_description": "Python"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Report generation failed. Please try again."
    assert "internal detail" not in response.text
