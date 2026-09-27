"""Data models for Job Skill Analyzer.

Defines domain models, enums, dataclasses, and serialization
methods used across the extraction, normalization, and reporting pipeline.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class SkillCategory(str, Enum):
    """Categorization taxonomy for recognized technical skills."""

    PROGRAMMING_LANGUAGE = "Programming Languages"
    FRAMEWORK = "Frameworks & Libraries"
    DATABASE = "Databases"
    CLOUD = "Cloud & Infrastructure"
    DEVOPS = "DevOps & CI/CD"
    API_BACKEND = "API & Backend"
    AI_DATA = "AI & Data Science"
    TOOLS = "Tools & Development"


class PriorityLevel(str, Enum):
    """Explainable priority levels for skill relevance or candidate gap closure."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass(frozen=True)
class SkillDefinition:
    """Canonical definition of a skill within the taxonomy.

    Attributes:
        name: The canonical, standardized name of the skill.
        category: The primary category to which the skill belongs.
        aliases: Common synonyms, acronyms, or variations for matching.
        default_weight: Heuristic importance weight used in priority analysis.
    """

    name: str
    category: SkillCategory
    aliases: tuple[str, ...] = ()
    default_weight: PriorityLevel = PriorityLevel.MEDIUM


@dataclass
class ExtractedSkill:
    """A recognized skill extracted from input text.

    Attributes:
        name: The canonical skill name.
        category: Skill category.
        matched_terms: The actual textual expressions matched in the document.
        frequency: Total number of times this skill was referenced.
    """

    name: str
    category: SkillCategory
    matched_terms: list[str] = field(default_factory=list)
    frequency: int = 1

    def to_dict(self) -> dict[str, Any]:
        """Convert extracted skill into a clean dictionary."""
        return {
            "name": self.name,
            "category": self.category.value,
            "matched_terms": self.matched_terms,
            "frequency": self.frequency,
        }


@dataclass
class PrioritizedSkill:
    """A skill evaluated with an explainable priority and rationale.

    Attributes:
        skill_name: The canonical skill name.
        category: Skill category.
        priority: Assessed priority level (High, Medium, Low).
        reason: Plain-language explanation for why this priority was assigned.
        is_missing: Whether this skill is currently missing from candidate profile.
    """

    skill_name: str
    category: SkillCategory
    priority: PriorityLevel
    reason: str
    is_missing: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert prioritized skill into a dictionary representation."""
        return {
            "skill": self.skill_name,
            "category": self.category.value,
            "priority": self.priority.value,
            "reason": self.reason,
            "is_missing": self.is_missing,
        }


@dataclass
class CandidateComparison:
    """Comparison results between job requirements and supplied candidate skills.

    Attributes:
        provided: Whether candidate skills were actually supplied.
        candidate_skills: Normalized candidate skills supplied by the user.
        matched_skills: Skills required by the job that the candidate possesses.
        missing_skills: Skills required by the job that the candidate lacks.
        match_percentage: Percentage of job skills matched (0.0 to 100.0).
    """

    provided: bool = False
    candidate_skills: list[str] = field(default_factory=list)
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    match_percentage: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert candidate comparison into dictionary representation."""
        return {
            "provided": self.provided,
            "candidate_skills": self.candidate_skills,
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "match_percentage": round(self.match_percentage, 1),
        }


@dataclass
class AnalysisReport:
    """Complete structured analysis output for a job description.

    Attributes:
        total_skills: Total number of distinct skills detected.
        skills: Detailed list of extracted skills.
        category_counts: Count of detected skills per category.
        candidate_comparison: Candidate skill comparison data, if provided.
        priorities: Evaluated priority breakdown with explainable reasons.
    """

    total_skills: int
    skills: list[ExtractedSkill]
    category_counts: dict[str, int]
    candidate_comparison: CandidateComparison
    priorities: list[PrioritizedSkill]

    def to_dict(self) -> dict[str, Any]:
        """Convert complete analysis report into serializable dictionary."""
        return {
            "total_skills": self.total_skills,
            "skills": [s.to_dict() for s in self.skills],
            "category_counts": self.category_counts,
            "candidate_comparison": self.candidate_comparison.to_dict(),
            "priorities": [p.to_dict() for p in self.priorities],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize complete analysis report into a JSON formatted string."""
        return json.dumps(self.to_dict(), indent=indent)
