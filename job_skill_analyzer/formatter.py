"""Presentation formatters for Job Skill Analyzer.

Provides clean CLI terminal output and a standalone HTML report generator
strictly adhering to the Career Intelligence Design System palette:
  --color-deep-navy:    #14252C
  --color-dark-slate:   #273C41
  --color-slate:        #45575B
  --color-light-gray:   #A3A39B
  --color-warm-cream:   #E6CAB3
  --color-burnt-orange: #82401D
"""

from __future__ import annotations

import sys
from typing import Dict, List

from job_skill_analyzer.models import (
    AnalysisReport,
    ExtractedSkill,
    PriorityLevel,
    SkillCategory,
)

# Design System Color Tokens
COLOR_DEEP_NAVY = "#14252C"
COLOR_DARK_SLATE = "#273C41"
COLOR_SLATE = "#45575B"
COLOR_LIGHT_GRAY = "#A3A39B"
COLOR_WARM_CREAM = "#E6CAB3"
COLOR_BURNT_ORANGE = "#82401D"


def _get_terminal_symbols() -> tuple[str, str, str]:
    """Return appropriate bullet symbols based on terminal encoding support."""
    try:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        "✓✗•".encode(encoding)
        return "✓", "✗", "•"
    except Exception:
        return "+", "-", "*"


def format_cli_report(report: AnalysisReport) -> str:
    """Format an AnalysisReport for clean, professional CLI presentation.

    Args:
        report: AnalysisReport instance.

    Returns:
        Structured multiline string ready for terminal display.
    """
    check_sym, cross_sym, bullet_sym = _get_terminal_symbols()

    lines: List[str] = [
        "=" * 50,
        "             JOB SKILL ANALYZER",
        "=" * 50,
        "",
        "ANALYSIS COMPLETE",
        f"Detected Skills: {report.total_skills}",
        "",
    ]

    if report.total_skills == 0:
        lines.append("No recognized technical skills were found in this job description.")
        lines.append("=" * 50)
        return "\n".join(lines)

    # Group skills by category
    skills_by_cat: Dict[str, List[ExtractedSkill]] = {}
    for skill in report.skills:
        skills_by_cat.setdefault(skill.category.value, []).append(skill)

    for cat_name, cat_skills in skills_by_cat.items():
        lines.append(cat_name.upper())
        for s in sorted(cat_skills, key=lambda x: x.name.lower()):
            freq_str = f" (x{s.frequency})" if s.frequency > 1 else ""
            lines.append(f"  {check_sym} {s.name}{freq_str}")
        lines.append("")

    lines.append("-" * 50)

    # Candidate Comparison & Gap Section
    comp = report.candidate_comparison
    if comp.provided:
        lines.append("SKILL GAP ANALYSIS")
        lines.append(f"Candidate Profile Match: {comp.match_percentage:.1f}%")
        lines.append(f"Matched Skills ({len(comp.matched_skills)}):")
        if comp.matched_skills:
            lines.append(f"  {check_sym} " + ", ".join(sorted(comp.matched_skills)))
        else:
            lines.append("  (None)")

        lines.append("")
        lines.append(f"Missing Skills ({len(comp.missing_skills)}):")
        if comp.missing_skills:
            lines.append(f"  {cross_sym} " + ", ".join(sorted(comp.missing_skills)))
        else:
            lines.append("  (All required skills matched!)")

        lines.append("")
        lines.append("RECOMMENDED LEARNING PRIORITIES")
        for level in (PriorityLevel.HIGH, PriorityLevel.MEDIUM, PriorityLevel.LOW):
            level_skills = [p for p in report.priorities if p.priority == level]
            if level_skills:
                lines.append(f"  [{level.value.upper()} PRIORITY]")
                for p in level_skills:
                    lines.append(f"    {bullet_sym} {p.skill_name} — {p.reason}")
    else:
        lines.append("SKILL EMPHASIS & PRIORITY (JOB POSTING)")
        for level in (PriorityLevel.HIGH, PriorityLevel.MEDIUM, PriorityLevel.LOW):
            level_skills = [p for p in report.priorities if p.priority == level]
            if level_skills:
                lines.append(f"  [{level.value.upper()} PRIORITY]")
                for p in level_skills:
                    lines.append(f"    {bullet_sym} {p.skill_name} — {p.reason}")
        lines.append("")
        lines.append("(Note: Supply candidate skills to view tailored gap analysis)")

    lines.append("=" * 50)
    return "\n".join(lines)


def generate_html_report(report: AnalysisReport, title: str = "Job Skill Analysis Report") -> str:
    """Generate a self-contained, responsive HTML report.

    Strictly applies the defined 6-color Career Intelligence palette:
      Deep Navy (#14252C) as page foundation,
      Dark Slate (#273C41) as card surfaces,
      Slate (#45575B) for borders and subtle dividers,
      Muted Light Gray (#A3A39B) for body & metadata,
      Warm Cream (#E6CAB3) for typography highlights and headers,
      Burnt Orange (#82401D) for high-priority badges and key callouts.

    Args:
        report: AnalysisReport instance.
        title: Document title.

    Returns:
        Full HTML5 document string.
    """
    comp = report.candidate_comparison

    # Render category skill cards
    skills_by_cat: Dict[str, List[ExtractedSkill]] = {}
    for skill in report.skills:
        skills_by_cat.setdefault(skill.category.value, []).append(skill)

    category_cards_html = ""
    for cat_name, cat_skills in skills_by_cat.items():
        skill_tags = "".join(
            f'<span class="skill-tag">{s.name}'
            f'{" <small class=\"freq\">(x" + str(s.frequency) + ")</small>" if s.frequency > 1 else ""}'
            f'</span>'
            for s in sorted(cat_skills, key=lambda x: x.name.lower())
        )
        category_cards_html += f"""
        <div class="card category-card">
            <h3>{cat_name}</h3>
            <div class="skill-tags-group">
                {skill_tags}
            </div>
        </div>
        """

    # Render candidate section
    if comp.provided:
        matched_tags = "".join(
            f'<span class="badge badge-matched">{s}</span>' for s in sorted(comp.matched_skills)
        ) or '<span class="empty-state">No matching skills detected</span>'

        missing_tags = "".join(
            f'<span class="badge badge-missing">{s}</span>' for s in sorted(comp.missing_skills)
        ) or '<span class="empty-state">No missing skills detected (100% matched!)</span>'

        candidate_section_html = f"""
        <div class="panel">
            <h2>Candidate Gap Analysis</h2>
            <div class="stat-banner">
                <div class="stat-item">
                    <span class="stat-number">{comp.match_percentage:.1f}%</span>
                    <span class="stat-label">Match Score</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(comp.matched_skills)}</span>
                    <span class="stat-label">Matched Skills</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(comp.missing_skills)}</span>
                    <span class="stat-label">Missing Skills</span>
                </div>
            </div>
            <div class="gap-grid">
                <div class="card">
                    <h3>Matched In Profile</h3>
                    <div class="badge-cluster">{matched_tags}</div>
                </div>
                <div class="card">
                    <h3>Skill Gaps to Address</h3>
                    <div class="badge-cluster">{missing_tags}</div>
                </div>
            </div>
        </div>
        """
    else:
        candidate_section_html = """
        <div class="panel">
            <h2>Candidate Gap Analysis</h2>
            <p class="muted-text">
                No candidate skills were provided. Provide candidate skills via CLI
                (<code>--candidate "Python, Docker"</code>) to calculate personalized match percentage and gaps.
            </p>
        </div>
        """

    # Render priority list
    priorities_html = ""
    for p in report.priorities:
        priority_class = f"priority-{p.priority.value.lower()}"
        priorities_html += f"""
        <div class="priority-row {priority_class}">
            <div class="priority-badge">{p.priority.value.upper()}</div>
            <div class="priority-info">
                <strong>{p.skill_name}</strong>
                <span class="priority-cat">({p.category.value})</span>
                <p class="priority-reason">{p.reason}</p>
            </div>
        </div>
        """

    if not priorities_html:
        priorities_html = '<div class="empty-state">No skills to prioritize.</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --color-deep-navy: {COLOR_DEEP_NAVY};
            --color-dark-slate: {COLOR_DARK_SLATE};
            --color-slate: {COLOR_SLATE};
            --color-light-gray: {COLOR_LIGHT_GRAY};
            --color-warm-cream: {COLOR_WARM_CREAM};
            --color-burnt-orange: {COLOR_BURNT_ORANGE};
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: var(--color-deep-navy);
            color: var(--color-warm-cream);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            padding: 2.5rem 1.5rem;
        }}
        .container {{
            max-width: 960px;
            margin: 0 auto;
        }}
        header {{
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--color-slate);
            padding-bottom: 1.5rem;
        }}
        h1 {{
            color: var(--color-warm-cream);
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .tagline {{
            color: var(--color-light-gray);
            font-size: 1.05rem;
            margin-top: 0.3rem;
        }}
        h2 {{
            color: var(--color-warm-cream);
            font-size: 1.4rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }}
        h3 {{
            color: var(--color-warm-cream);
            font-size: 1.05rem;
            margin-bottom: 0.8rem;
            font-weight: 600;
        }}
        .panel {{
            background-color: var(--color-dark-slate);
            border: 1px solid var(--color-slate);
            border-radius: 20px;
            padding: 1.75rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        }}
        .card {{
            background-color: rgba(20, 37, 44, 0.6);
            border: 1px solid var(--color-slate);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }}
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.2rem;
        }}
        .gap-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.2rem;
            margin-top: 1.2rem;
        }}
        @media (max-width: 640px) {{
            .gap-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        .skill-tags-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .skill-tag {{
            background-color: var(--color-dark-slate);
            color: var(--color-warm-cream);
            border: 1px solid var(--color-slate);
            border-radius: 8px;
            padding: 0.35rem 0.75rem;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        .freq {{
            color: var(--color-light-gray);
            font-size: 0.75rem;
            margin-left: 0.25rem;
        }}
        .stat-banner {{
            display: flex;
            gap: 2rem;
            padding: 1rem 0;
            border-bottom: 1px solid var(--color-slate);
        }}
        .stat-item {{
            display: flex;
            flex-direction: column;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-warm-cream);
        }}
        .stat-label {{
            font-size: 0.85rem;
            color: var(--color-light-gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-cluster {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .badge {{
            padding: 0.3rem 0.7rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .badge-matched {{
            background-color: rgba(69, 87, 91, 0.4);
            border: 1px solid var(--color-slate);
            color: var(--color-warm-cream);
        }}
        .badge-missing {{
            background-color: rgba(130, 64, 29, 0.25);
            border: 1px solid var(--color-burnt-orange);
            color: var(--color-warm-cream);
        }}
        .priority-row {{
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            padding: 0.85rem 1rem;
            border-radius: 12px;
            background-color: rgba(20, 37, 44, 0.5);
            border: 1px solid var(--color-slate);
            margin-bottom: 0.75rem;
        }}
        .priority-badge {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }}
        .priority-high .priority-badge {{
            background-color: var(--color-burnt-orange);
            color: var(--color-warm-cream);
        }}
        .priority-medium .priority-badge {{
            background-color: var(--color-slate);
            color: var(--color-warm-cream);
        }}
        .priority-low .priority-badge {{
            background-color: rgba(69, 87, 91, 0.3);
            color: var(--color-light-gray);
            border: 1px solid var(--color-slate);
        }}
        .priority-info strong {{
            color: var(--color-warm-cream);
            font-size: 0.95rem;
        }}
        .priority-cat {{
            color: var(--color-light-gray);
            font-size: 0.85rem;
            margin-left: 0.3rem;
        }}
        .priority-reason {{
            color: var(--color-light-gray);
            font-size: 0.85rem;
            margin-top: 0.2rem;
        }}
        .muted-text {{
            color: var(--color-light-gray);
        }}
        .empty-state {{
            color: var(--color-light-gray);
            font-style: italic;
            padding: 0.5rem 0;
        }}
        code {{
            background-color: var(--color-deep-navy);
            border: 1px solid var(--color-slate);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            color: var(--color-warm-cream);
            font-family: monospace;
            font-size: 0.85rem;
        }}
        footer {{
            text-align: center;
            margin-top: 3rem;
            color: var(--color-light-gray);
            font-size: 0.85rem;
            border-top: 1px solid var(--color-slate);
            padding-top: 1.5rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Job Skill Analyzer</h1>
            <p class="tagline">Career Intelligence & Rule-Based Technical Skill Extraction</p>
        </header>

        <section class="panel">
            <h2>Extracted Job Skills ({report.total_skills})</h2>
            <div class="card-grid">
                {category_cards_html}
            </div>
        </section>

        {candidate_section_html}

        <section class="panel">
            <h2>Priority Analysis & Methodology</h2>
            <p class="muted-text" style="margin-bottom: 1.2rem;">
                Deterministic priority ranking calculated from mention frequency,
                core architectural categorization, and missing profile competencies.
            </p>
            {priorities_html}
        </section>

        <footer>
            Generated by Job Skill Analyzer &bull; Deterministic NLP &bull; Professional Career Intelligence
        </footer>
    </div>
</body>
</html>
"""
    return html
