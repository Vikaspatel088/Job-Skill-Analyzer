"""Command-line interface (CLI) for Job Skill Analyzer.

Provides interactive and batch processing of job descriptions and candidate skills,
with plain terminal, machine-readable JSON, and standalone HTML outputs.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from job_skill_analyzer.analyzer import JobSkillAnalyzer
from job_skill_analyzer.formatter import format_cli_report, generate_html_report


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="job-skill-analyzer",
        description="Analyze job descriptions, extract technical skills, and perform gap analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze job description from a file
  python -m job_skill_analyzer --file job.txt

  # Compare against candidate skills
  python -m job_skill_analyzer --file job.txt --candidate "Python, Docker, React"

  # Machine-readable JSON output
  python -m job_skill_analyzer --file job.txt --json

  # Export standalone HTML report
  python -m job_skill_analyzer --file job.txt --html report.html

  # Interactive mode
  python -m job_skill_analyzer
        """,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to job description text file.",
    )
    parser.add_argument(
        "-c",
        "--candidate",
        type=str,
        help="Comma-separated candidate skills (e.g. 'Python, Docker, AWS').",
    )
    parser.add_argument(
        "--candidate-file",
        type=str,
        help="Path to file containing candidate skills (one per line or comma-separated).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured analysis in valid JSON format to stdout.",
    )
    parser.add_argument(
        "--html",
        type=str,
        help="Save complete visual report to the specified HTML file path.",
    )
    return parser


def read_file_safely(file_path_str: str, file_label: str = "Job description") -> str:
    """Read file contents with clean user-facing error handling.

    Args:
        file_path_str: Path to file.
        file_label: User-friendly label for error messages.

    Returns:
        Content of the file.

    Raises:
        ValueError: If file does not exist, cannot be read, or is empty.
    """
    path = Path(file_path_str)
    if not path.exists():
        raise ValueError(f"{file_label} file not found: '{file_path_str}'")
    if not path.is_file():
        raise ValueError(f"Path is not a regular file: '{file_path_str}'")

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding="latin-1")
        except Exception as exc:
            raise ValueError(f"Unable to read {file_label.lower()} file '{file_path_str}': {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Unable to read {file_label.lower()} file '{file_path_str}': {exc}") from exc

    if not content or not content.strip():
        raise ValueError(f"{file_label} file is empty: '{file_path_str}'")

    return content


def prompt_for_interactive_input() -> tuple[str, Optional[str]]:
    """Prompt user interactively for job description and candidate skills."""
    print("=" * 50)
    print("             JOB SKILL ANALYZER")
    print("=" * 50)
    print("Paste or type the job description below.")
    print("(Press Ctrl+Z then Enter on Windows, or Ctrl+D on Unix, to submit):")
    print("-" * 50)

    try:
        job_lines = sys.stdin.read()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

    if not job_lines or not job_lines.strip():
        raise ValueError("No job description text was provided.")

    print("\n" + "-" * 50)
    print("Optional: Enter candidate skills (comma-separated), or press Enter to skip:")
    try:
        # Re-open console input if stdin was closed by EOF
        if sys.platform == "win32":
            with open("CONIN$", "r", encoding="utf-8") as conin:
                candidate_input = conin.readline().strip()
        else:
            with open("/dev/tty", "r", encoding="utf-8") as tty:
                candidate_input = tty.readline().strip()
    except Exception:
        candidate_input = None

    candidate_skills = candidate_input if candidate_input else None
    return job_lines, candidate_skills


def main(args: Optional[list[str]] = None) -> int:
    """CLI application entry point.

    Args:
        args: Optional command line argument list (defaults to sys.argv[1:]).

    Returns:
        Process exit code (0 for success, non-zero for error).
    """
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = build_parser()
    parsed_args = parser.parse_args(args)

    try:
        # 1. Obtain job description text
        if parsed_args.file:
            job_text = read_file_safely(parsed_args.file, "Job description")
        else:
            # Check if stdin has piped input
            if not sys.stdin.isatty():
                job_text = sys.stdin.read()
                if not job_text or not job_text.strip():
                    raise ValueError("Piped input job description is empty.")
            else:
                job_text, interactive_candidate = prompt_for_interactive_input()
                if interactive_candidate and not parsed_args.candidate:
                    parsed_args.candidate = interactive_candidate

        # 2. Obtain candidate skills
        candidate_skills: Optional[str] = None
        if parsed_args.candidate:
            candidate_skills = parsed_args.candidate
        elif parsed_args.candidate_file:
            candidate_skills = read_file_safely(parsed_args.candidate_file, "Candidate skills")

        # 3. Run analysis pipeline
        analyzer = JobSkillAnalyzer()
        report = analyzer.analyze(job_text, candidate_skills=candidate_skills)

        # 4. Handle output formats
        if parsed_args.json:
            print(report.to_json(indent=2))
        else:
            print(format_cli_report(report))

        # 5. Handle HTML output export if requested
        if parsed_args.html:
            html_content = generate_html_report(report)
            out_path = Path(parsed_args.html)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html_content, encoding="utf-8")
            if not parsed_args.json:
                print(f"\nHTML report saved successfully to: {out_path.resolve()}")

        return 0

    except ValueError as err:
        sys.stderr.write(f"Error: {err}\n")
        return 1
    except Exception as err:
        # If debugging is explicitly requested via environment variable, show full trace
        if os.getenv("DEBUG") == "1":
            raise
        sys.stderr.write(f"Unexpected error: {err}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
