"""FastAPI REST API layer for Job Skill Analyzer.

Exposes the core deterministic Python NLP engine as a typed REST service
without duplicating any extraction, normalization, or scoring logic.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from job_skill_analyzer.analyzer import JobSkillAnalyzer
from job_skill_analyzer.formatter import generate_html_report

# Initialize shared analyzer instance (single source of truth)
analyzer = JobSkillAnalyzer()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Job Skill Analyzer API",
    description="Deterministic rule-based NLP service for technical skill extraction and gap analysis.",
    version="1.0.0",
)

# Configure CORS for local development & frontend hosting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """Payload for job description analysis."""

    job_description: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
        description="Raw job posting text to extract skills from.",
        examples=["Looking for a Senior Python engineer with FastAPI, PostgreSQL, and Docker experience."],
    )
    candidate_skills: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Optional candidate skills as a comma-separated string or list of strings.",
        examples=["Python, FastAPI, Docker"],
    )


class HealthResponse(BaseModel):
    """Health status response."""

    status: str
    version: str


class SkillResponse(BaseModel):
    name: str
    category: str
    matched_terms: List[str]
    frequency: int


class CandidateComparisonResponse(BaseModel):
    provided: bool
    candidate_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float


class PriorityResponse(BaseModel):
    skill: str
    category: str
    priority: str
    reason: str
    is_missing: bool


class AnalysisDataResponse(BaseModel):
    total_skills: int
    skills: List[SkillResponse]
    category_counts: dict[str, int]
    candidate_comparison: CandidateComparisonResponse
    priorities: List[PriorityResponse]


class AnalyzeResponse(BaseModel):
    success: bool
    data: AnalysisDataResponse


class SampleResponse(BaseModel):
    job_description: str
    candidate_skills: str
    role_title: str


@app.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.get("/api/sample", response_model=SampleResponse)
def get_sample_data() -> SampleResponse:
    """Provide realistic sample job description and candidate profiles for quick exploration."""
    return SampleResponse(
        job_description=(
            "Senior Backend & Platform Engineer\n\n"
            "We are seeking an experienced Backend Engineer to scale our distributed microservices. "
            "You will design asynchronous APIs using Python and FastAPI, optimizing relational data models "
            "in PostgreSQL. The role requires containerizing services with Docker and orchestrating deployments "
            "via Kubernetes. You will manage cloud infrastructure on AWS, leveraging EC2, S3, and Lambda functions. "
            "Experience with REST API design, Git version control, and automated CI/CD pipelines using GitHub Actions "
            "is required. Familiarity with Redis caching and Machine Learning fundamentals is a strong plus."
        ),
        candidate_skills="Python, FastAPI, PostgreSQL, Docker, Git, REST API, Redis",
        role_title="Senior Backend & Platform Engineer",
    )


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_job(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Execute the NLP pipeline on a job description and return structured analysis."""
    text = payload.job_description.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Job description cannot be empty or whitespace only.",
        )

    try:
        report = analyzer.analyze(
            job_description=text,
            candidate_skills=payload.candidate_skills,
        )
        return AnalyzeResponse(success=True, data=report.to_dict())
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err),
        ) from err
    except Exception as err:
        logger.exception("Job analysis failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed. Please try again.",
        ) from err


@app.post("/api/report/html", response_class=HTMLResponse)
def generate_html(payload: AnalyzeRequest) -> HTMLResponse:
    """Generate a standalone, self-contained HTML report strictly using the design system."""
    text = payload.job_description.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Job description cannot be empty or whitespace only.",
        )

    try:
        report = analyzer.analyze(
            job_description=text,
            candidate_skills=payload.candidate_skills,
        )
        html_content = generate_html_report(report)
        return HTMLResponse(content=html_content, status_code=200)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err),
        ) from err
    except Exception as err:
        logger.exception("HTML report generation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Report generation failed. Please try again.",
        ) from err


# Mount static production build if present
dist_path = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if dist_path.exists():
    app.mount("/", StaticFiles(directory=str(dist_path), html=True), name="static")
