import json
from pathlib import Path
import pytest
from src.reporter import ReportGenerator
@pytest.fixture
def sample_match_results():
    """Standard sample comparison results dictionary."""
    return {
        "match_percentage": 75.0,
        "matched_skills": ["django", "docker", "python"],
        "missing_skills": ["aws"],
        "total_job_skills": 4,
    }
class TestReportGeneratorTerminal:
    def test_terminal_report_content(self, sample_match_results):
        report = ReportGenerator.generate_terminal_report(
        sample_match_results, use_color=False
        )
        assert "SKILL MATCH REPORT: 75.0% Match" in report
        assert "Total In-Demand Skills Detected: 4" in report
        assert "Matched Candidate Skills (3):" in report
        assert "✓ django" in report
        assert "✓ docker" in report
        assert "✓ python" in report
        assert "Missing Skills to Acquire (1):" in report
        assert "✗ aws" in report
    def test_terminal_report_no_color_has_no_ansi(self, sample_match_results):
        report = ReportGenerator.generate_terminal_report(
            sample_match_results, use_color=False
        )
        assert "\033[" not in report
    def test_terminal_report_with_color_ansi_present(self, sample_match_results):
        report = ReportGenerator.generate_terminal_report(
            sample_match_results, use_color=True
        )
        assert "\033[" in report
        assert ReportGenerator.GREEN in report
    def test_terminal_report_medium_match_color(self):
        results = {
            "match_percentage": 50.0,
            "matched_skills": ["python"],
            "missing_skills": ["django"],
            "total_job_skills": 2,
        }
        report = ReportGenerator.generate_terminal_report(results, use_color=True)
        assert ReportGenerator.CYAN in report
    def test_terminal_report_low_match_color(self):
        results = {
            "match_percentage": 20.0,
            "matched_skills": ["git"],
            "missing_skills": ["python", "django", "aws", "docker"],
            "total_job_skills": 5,
        }
        report = ReportGenerator.generate_terminal_report(results, use_color=True)
        assert ReportGenerator.RED in report
    def test_terminal_report_empty_skills_branches(self):
        empty_results = {
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "total_job_skills": 0,
        }
        report = ReportGenerator.generate_terminal_report(
            empty_results, use_color=False
        )
        assert "(None)" in report
        assert "(None - Candidate meets all required skills!)" in report
class TestReportGeneratorExports:
    def test_export_json(self, tmp_path, sample_match_results):
        target_file = tmp_path / "nested" / "output_report.json"
        ReportGenerator.export_json(sample_match_results, target_file)
        assert target_file.exists()
        with open(target_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        assert loaded_data == sample_match_results
        assert loaded_data["match_percentage"] == 75.0
        assert loaded_data["matched_skills"] == ["django", "docker", "python"]
    def test_export_markdown(self, tmp_path, sample_match_results):
        target_file = tmp_path / "nested" / "output_report.md"
        ReportGenerator.export_markdown(sample_match_results, target_file)
        assert target_file.exists()
        content = target_file.read_text(encoding="utf-8")
        assert "# Skill Gap Analysis Report" in content
        assert "**Match Rating:** 75.0%" in content
        assert "**Total Required Skills Identified:** 4" in content
        assert "## Matched Skills" in content
        assert "- [x] `django`" in content
        assert "- [x] `docker`" in content
        assert "- [x] `python`" in content
        assert "## Missing Skills (Recommended Focus Areas)" in content
        assert "- [ ] `aws`" in content
        assert "*Report generated automatically by tech-skill-matcher-cli.*" in content
    def test_export_markdown_empty_skills(self, tmp_path):
        target_file = tmp_path / "empty_report.md"
        empty_results = {
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "total_job_skills": 0,
        }
        ReportGenerator.export_markdown(empty_results, target_file)
        assert target_file.exists()
        content = target_file.read_text(encoding="utf-8")
        assert "- *No overlapping skills found.*" in content
        assert "- *No missing skills.*" in content


