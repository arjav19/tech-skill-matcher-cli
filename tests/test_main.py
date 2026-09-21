import json
import subprocess
import sys
from pathlib import Path
import pytest

class TestCLIItegration:

    @pytest.fixture
    def project_root(self):
        return Path(__file__).parent.parent

    def test_cli_with_sample_files(self, project_root):
        sample_file = project_root / "data" / "sample_jobs" / "backend_django.txt"
        if not sample_file.exists():
            pytest.skip("Sample file not yet created")

        cmd  = [
            sys.executable,
            str(project_root / "main.py"),
            "--file",
            str(sample_file),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)


        assert result.returncode == 0
        assert "SKILL MATCH REPORT" in result.stdout
        assert "Matched Skills" in result.stdout


    def test_cli_json_flag_output(self, project_root):
        sample_file = project_root / "data" / "sample_jobs" / "backend_django.txt"
        if not sample_file.exists():
            pytest.skip("Sample file not yet created")


        cmd = [
            sys.executable,
            str(project_root / "main.py"),
            "--file",
            str(sample_file),
            "--json",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)


        assert result.returncode == 0
        # Output must be valid parseable JSON
        data = json.loads(result.stdout)
        assert "match_percentage" in data
        assert "matched_skills" in data
        assert "missing_skills" in data
        assert isinstance(data["match_percentage"], (int, float))


    def test_cli_missing_arguments_fails(self, project_root):
        # Running without --file or --url should exit with non-zero code
        cmd = [sys.executable, str(project_root / "main.py")]
        result = subprocess.run(cmd, capture_output=True, text=True)


        assert result.returncode != 0
        assert "Error: Please provide either --file or --url" in result.stderr

