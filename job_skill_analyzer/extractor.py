"""Skill extraction engine using deterministic rule-based boundary matching.

Extracts canonical technical skills from preprocessed text, handling
multi-word phrases, specialized punctuation (C++, C#, .NET, CI/CD),
case-insensitivity, and overlapping token disambiguation.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from job_skill_analyzer.models import ExtractedSkill
from job_skill_analyzer.normalizer import clean_text
from job_skill_analyzer.taxonomy import (
    SKILL_DEFINITIONS,
    get_canonical_map,
    get_definition_map,
)


class SkillExtractor:
    """Deterministic extractor for technical skills from job descriptions.

    Compiles optimized boundary regex patterns for each known skill term
    and alias, matching longer multi-word phrases first and disambiguating
    overlapping character spans.
    """

    def __init__(self) -> None:
        self._canonical_map: Dict[str, str] = get_canonical_map()
        self._definition_map = get_definition_map()
        # Compile patterns sorted by descending length to prioritize longer phrases
        self._compiled_patterns: List[Tuple[str, re.Pattern[str]]] = self._build_patterns()

    def _build_patterns(self) -> List[Tuple[str, re.Pattern[str]]]:
        """Compile regex patterns for all taxonomy terms and aliases."""
        patterns: List[Tuple[str, re.Pattern[str]]] = []
        # Sort keys by length descending to prioritize phrases like "REST API" over "API"
        sorted_terms = sorted(self._canonical_map.keys(), key=len, reverse=True)

        for term in sorted_terms:
            # Word boundary definition that handles special characters:
            # If term begins with non-alphanumeric (e.g. '.net'), don't require non-punct before
            prefix = r"(?<![a-zA-Z0-9])" if not term[0].isalnum() else r"(?<![a-zA-Z0-9_#+])"
            # Suffix prevents matching substring of larger word (e.g. 'go' in 'good' or 'c' in 'cat')
            suffix = r"(?![a-zA-Z0-9_#+])"
            pattern = re.compile(prefix + re.escape(term) + suffix, re.IGNORECASE)
            patterns.append((term, pattern))

        return patterns

    def extract(self, text: str) -> List[ExtractedSkill]:
        """Extract all recognized canonical skills from input text.

        Args:
            text: Raw or preprocessed job description text.

        Returns:
            List of ExtractedSkill instances with canonical names,
            categories, matched terms, and mention frequencies.
        """
        if not text or not text.strip():
            return []

        cleaned = clean_text(text)
        if not cleaned:
            return []

        # Find all raw pattern matches with their character spans
        raw_matches: List[Tuple[int, int, str, str]] = []
        for term, pattern in self._compiled_patterns:
            for match in pattern.finditer(cleaned):
                start, end = match.span()
                matched_text = match.group(0)
                raw_matches.append((start, end, term, matched_text))

        # Sort matches primarily by start index, and secondarily by span length (descending)
        raw_matches.sort(key=lambda m: (m[0], -(m[1] - m[0])))

        # Resolve overlapping spans greedily (longer matches taking precedence)
        accepted_spans: List[Tuple[int, int, str, str]] = []
        for start, end, term, matched_text in raw_matches:
            # Check if this span overlaps with any previously accepted span
            overlaps = any(max(start, s) < min(end, e) for s, e, _, _ in accepted_spans)
            if not overlaps:
                accepted_spans.append((start, end, term, matched_text))

        # Aggregate matches into canonical skills
        skills_by_canonical: Dict[str, ExtractedSkill] = {}

        for _, _, term, matched_text in accepted_spans:
            canonical_name = self._canonical_map[term]
            definition = self._definition_map[canonical_name]

            if canonical_name not in skills_by_canonical:
                skills_by_canonical[canonical_name] = ExtractedSkill(
                    name=canonical_name,
                    category=definition.category,
                    matched_terms=[matched_text],
                    frequency=1,
                )
            else:
                existing = skills_by_canonical[canonical_name]
                existing.frequency += 1
                if matched_text not in existing.matched_terms:
                    existing.matched_terms.append(matched_text)

        # Return skills sorted consistently (descending frequency, then alphabetical)
        return sorted(
            skills_by_canonical.values(),
            key=lambda s: (-s.frequency, s.name.lower()),
        )
