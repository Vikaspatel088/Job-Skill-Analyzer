"""Tests for Command-Line Interface (CLI)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from job_skill_analyzer.cli import main


def test_cli_with_valid_file_and_candidate(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    job_file = tmp_path / "job.txt"
    job_file.write_text("Looking for Python, FastAPI, and Docker.", encoding="utf-8")

    exit_code = main(["--file", str(job_file), "--candidate", "Python, Docker"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "JOB SKILL ANALYZER" in captured.out
    assert "Python" in captured.out
    assert "FastAPI" in captured.out
    assert "SKILL GAP ANALYSIS" in captured.out


def test_cli_json_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    job_file = tmp_path / "job.txt"
    job_file.write_text("Skills needed: Python, AWS, Docker.", encoding="utf-8")

    exit_code = main(["--file", str(job_file), "--json"])
    assert exit_code == 0

    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed["total_skills"] == 3
    names = {s["name"] for s in parsed["skills"]}
    assert names == {"Python", "AWS", "Docker"}


def test_cli_html_output_export(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    job_file = tmp_path / "job.txt"
    job_file.write_text("Skills needed: Python, AWS.", encoding="utf-8")
    html_out = tmp_path / "report.html"

    exit_code = main(["--file", str(job_file), "--html", str(html_out)])
    assert exit_code == 0
    assert html_out.exists()
    html_content = html_out.read_text(encoding="utf-8")
    assert "--color-deep-navy: #14252C" in html_content
    assert "Python" in html_content


def test_cli_nonexistent_file_exits_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--file", "nonexistent_file_12345.txt"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error: Job description file not found" in captured.err
    # Verify no unhandled traceback exposed
    assert "Traceback" not in captured.err


def test_cli_empty_file_exits_cleanly(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("   \n  \t ", encoding="utf-8")

    exit_code = main(["--file", str(empty_file)])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error: Job description file is empty" in captured.err


def test_cli_candidate_file_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    job_file = tmp_path / "job.txt"
    job_file.write_text("Requires Python, AWS, and Docker.", encoding="utf-8")

    cand_file = tmp_path / "candidate.txt"
    cand_file.write_text("Python\nDocker\n", encoding="utf-8")

    exit_code = main(["--file", str(job_file), "--candidate-file", str(cand_file)])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Matched Skills (2)" in captured.out
    assert "Missing Skills (1)" in captured.out
