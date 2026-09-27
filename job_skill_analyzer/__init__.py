"""Job Skill Analyzer.

A rule-based NLP tool for extracting, normalizing, categorizing technical
skills from job descriptions, and performing candidate gap analysis.
"""

from job_skill_analyzer.analyzer import JobSkillAnalyzer
from job_skill_analyzer.extractor import SkillExtractor
from job_skill_analyzer.models import (
    AnalysisReport,
    CandidateComparison,
    ExtractedSkill,
    PriorityLevel,
    PrioritizedSkill,
    SkillCategory,
    SkillDefinition,
)
from job_skill_analyzer.normalizer import (
    clean_text,
    normalize_skill_name,
    parse_and_normalize_skills,
)

__version__ = "1.0.0"

__all__ = [
    "AnalysisReport",
    "CandidateComparison",
    "ExtractedSkill",
    "JobSkillAnalyzer",
    "PrioritizedSkill",
    "PriorityLevel",
    "SkillCategory",
    "SkillDefinition",
    "SkillExtractor",
    "clean_text",
    "normalize_skill_name",
    "parse_and_normalize_skills",
]
