"""Text preprocessing and skill normalization utilities.

Provides functions to clean input text, normalize skill aliases to
canonical taxonomy names, and process candidate skill inputs.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional

from job_skill_analyzer.taxonomy import get_canonical_map


def clean_text(text: str) -> str:
    """Preprocess and clean input text for NLP extraction.

    Normalizes irregular whitespace, unicode punctuation (such as typographic
    quotes or dashes), and non-printable characters while preserving
    important programming characters (+, #, ., /, -).

    Args:
        text: Raw text string.

    Returns:
        Cleaned text string.
    """
    if not text:
        return ""

    # Normalize typographic dashes and quotes
    cleaned = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015]", "-", text)
    cleaned = re.sub(r"[\u2018\u2019]", "'", cleaned)
    cleaned = re.sub(r"[\u201C\u201D]", '"', cleaned)

    # Normalize excessive carriage returns / newlines and tabs to standard spaces
    cleaned = re.sub(r"[\r\n\t]+", " ", cleaned)
    # Collapse multiple spaces into single space
    cleaned = re.sub(r" {2,}", " ", cleaned)

    return cleaned.strip()


def normalize_skill_name(raw_name: str) -> Optional[str]:
    """Normalize a raw skill string or alias to its canonical name.

    Examples:
        'postgres' -> 'PostgreSQL'
        'js' -> 'JavaScript'
        'k8s' -> 'Kubernetes'
        'gcp' -> 'Google Cloud'
        'sklearn' -> 'scikit-learn'

    Args:
        raw_name: The raw term or alias string.

    Returns:
        Canonical skill name if recognized in taxonomy, else None.
    """
    if not raw_name:
        return None

    cleaned = raw_name.strip().lower()
    canonical_map = get_canonical_map()

    # Exact alias/canonical lookup
    if cleaned in canonical_map:
        return canonical_map[cleaned]

    # Try stripping surrounding punctuation (e.g. trailing period or comma)
    stripped = cleaned.strip(".,;:!?()[]{}'\"")
    if stripped in canonical_map:
        return canonical_map[stripped]

    return None


def parse_and_normalize_skills(skill_inputs: str | Iterable[str]) -> List[str]:
    """Parse comma, semicolon, or newline-separated candidate skill strings.

    Normalizes recognized aliases into their canonical taxonomy names,
    deduplicates entries while preserving order, and cleans unknown skills.

    Args:
        skill_inputs: A comma-separated string or list/iterable of strings.

    Returns:
        List of distinct, normalized skill names.
    """
    if not skill_inputs:
        return []

    tokens: List[str] = []
    if isinstance(skill_inputs, str):
        # Split on commas, semicolons, or newlines
        raw_tokens = re.split(r"[,;\n\r]+", skill_inputs)
        tokens = [t.strip() for t in raw_tokens if t.strip()]
    else:
        for item in skill_inputs:
            if isinstance(item, str):
                parts = re.split(r"[,;\n\r]+", item)
                tokens.extend(p.strip() for p in parts if p.strip())

    normalized_list: List[str] = []
    seen: set[str] = set()

    for token in tokens:
        canonical = normalize_skill_name(token)
        chosen = canonical if canonical else token
        key = chosen.lower()
        if key not in seen:
            seen.add(key)
            normalized_list.append(chosen)

    return normalized_list
