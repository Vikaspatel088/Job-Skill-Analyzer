"""Core pipeline orchestration for Job Skill Analyzer.

Coordinates preprocessing, extraction, normalization, categorization,
candidate gap comparison, and deterministic priority scoring into a
cohesive, type-safe analysis workflow.
"""

from __future__ import annotations

from typing import Iterable, List, Optional

from job_skill_analyzer.extractor import SkillExtractor
from job_skill_analyzer.models import (
    AnalysisReport,
    CandidateComparison,
    ExtractedSkill,
    PriorityLevel,
    PrioritizedSkill,
    SkillCategory,
)
from job_skill_analyzer.normalizer import clean_text, parse_and_normalize_skills
from job_skill_analyzer.taxonomy import get_definition_map


class JobSkillAnalyzer:
    """Orchestrates end-to-end skill analysis of job postings.

    Attributes:
        extractor: Reusable rule-based SkillExtractor instance.
    """

    def __init__(self, extractor: Optional[SkillExtractor] = None) -> None:
        self.extractor = extractor or SkillExtractor()
        self._definition_map = get_definition_map()

    def analyze(
        self,
        job_description: str,
        candidate_skills: Optional[str | Iterable[str]] = None,
    ) -> AnalysisReport:
        """Execute the complete analysis pipeline on a job description.

        Pipeline stages:
            1. Input validation & text preprocessing
            2. Skill extraction with boundary regex matching
            3. Normalization & category aggregation
            4. Candidate gap comparison (if candidate skills supplied)
            5. Deterministic, explainable priority calculation

        Args:
            job_description: Full text of the job posting.
            candidate_skills: Optional comma-separated string or iterable of
                candidate skills to compare against requirements.

        Returns:
            Structured AnalysisReport containing all extracted skills,
            category distribution, gap analysis, and priority rankings.

        Raises:
            ValueError: If job_description is empty or contains only whitespace.
        """
        if not job_description or not job_description.strip():
            raise ValueError("Job description cannot be empty or whitespace only.")

        cleaned_text = clean_text(job_description)
        extracted_skills = self.extractor.extract(cleaned_text)

        # Categorization aggregation
        category_counts: dict[str, int] = {}
        for skill in extracted_skills:
            cat_name = skill.category.value
            category_counts[cat_name] = category_counts.get(cat_name, 0) + 1

        # Candidate comparison and gap analysis
        candidate_comp = self._evaluate_candidate_gap(
            extracted_skills, candidate_skills
        )

        # Deterministic priority analysis
        priorities = self._evaluate_priorities(extracted_skills, candidate_comp)

        return AnalysisReport(
            total_skills=len(extracted_skills),
            skills=extracted_skills,
            category_counts=category_counts,
            candidate_comparison=candidate_comp,
            priorities=priorities,
        )

    def _evaluate_candidate_gap(
        self,
        job_skills: List[ExtractedSkill],
        candidate_input: Optional[str | Iterable[str]],
    ) -> CandidateComparison:
        """Compare extracted job skills against supplied candidate skills.

        Note: If candidate_input is None or empty, candidate comparison
        is marked as not provided (provided=False) to avoid false assertions
        about what a candidate lacks.
        """
        if candidate_input is None:
            return CandidateComparison(provided=False)

        normalized_candidate = parse_and_normalize_skills(candidate_input)
        if not normalized_candidate:
            return CandidateComparison(
                provided=True,
                candidate_skills=[],
                matched_skills=[],
                missing_skills=[s.name for s in job_skills],
                match_percentage=0.0,
            )

        candidate_set = {s.lower() for s in normalized_candidate}

        matched: List[str] = []
        missing: List[str] = []

        for skill in job_skills:
            if skill.name.lower() in candidate_set:
                matched.append(skill.name)
            else:
                missing.append(skill.name)

        total_reqs = len(job_skills)
        pct = (len(matched) / total_reqs * 100.0) if total_reqs > 0 else 0.0

        return CandidateComparison(
            provided=True,
            candidate_skills=normalized_candidate,
            matched_skills=matched,
            missing_skills=missing,
            match_percentage=pct,
        )

    def _evaluate_priorities(
        self,
        job_skills: List[ExtractedSkill],
        comparison: CandidateComparison,
    ) -> List[PrioritizedSkill]:
        """Calculate explainable skill priorities deterministically.

        Methodology:
        - When candidate skills are provided:
          Evaluates missing skills to guide candidate preparation.
          * Frequency >= 2 -> HIGH (frequently emphasized in posting).
          * Core categories (Cloud, Languages, Databases) -> HIGH.
          * Mid-tier categories (Frameworks, DevOps, Backend APIs, AI) -> MEDIUM.
          * Auxiliary categories (Tools & Development) -> LOW.
        - When candidate skills are NOT provided:
          Evaluates all detected job requirements based on posting prominence
          and technical foundational weight.
        """
        priorities: List[PrioritizedSkill] = []
        skills_by_name = {s.name: s for s in job_skills}

        if comparison.provided:
            # Prioritize missing skills for the candidate
            for name in comparison.missing_skills:
                skill = skills_by_name[name]
                level, reason = self._compute_skill_priority(skill, is_missing=True)
                priorities.append(
                    PrioritizedSkill(
                        skill_name=skill.name,
                        category=skill.category,
                        priority=level,
                        reason=reason,
                        is_missing=True,
                    )
                )
        else:
            # Prioritize all detected job skills
            for skill in job_skills:
                level, reason = self._compute_skill_priority(skill, is_missing=False)
                priorities.append(
                    PrioritizedSkill(
                        skill_name=skill.name,
                        category=skill.category,
                        priority=level,
                        reason=reason,
                        is_missing=False,
                    )
                )

        # Sort priorities: High first, then Medium, then Low; secondary by skill name
        priority_order = {PriorityLevel.HIGH: 0, PriorityLevel.MEDIUM: 1, PriorityLevel.LOW: 2}
        priorities.sort(key=lambda p: (priority_order[p.priority], p.skill_name.lower()))
        return priorities

    def _compute_skill_priority(
        self, skill: ExtractedSkill, is_missing: bool
    ) -> tuple[PriorityLevel, str]:
        """Compute the deterministic priority level and explanation for a single skill."""
        freq = skill.frequency
        cat = skill.category

        if freq >= 2:
            return (
                PriorityLevel.HIGH,
                f"High posting emphasis ({freq} mentions in description).",
            )

        # Cloud and core programming languages and databases form technical pillars
        if cat in (
            SkillCategory.CLOUD,
            SkillCategory.PROGRAMMING_LANGUAGE,
            SkillCategory.DATABASE,
        ):
            return (
                PriorityLevel.HIGH,
                f"Core architectural foundation ({cat.value}).",
            )

        if cat in (
            SkillCategory.FRAMEWORK,
            SkillCategory.DEVOPS,
            SkillCategory.API_BACKEND,
            SkillCategory.AI_DATA,
        ):
            return (
                PriorityLevel.MEDIUM,
                f"Standard technical requirement ({cat.value}).",
            )

        # Tools & Development (Git, GitHub, Linux, etc.)
        return (
            PriorityLevel.LOW,
            f"Supporting tooling and environment ({cat.value}).",
        )
