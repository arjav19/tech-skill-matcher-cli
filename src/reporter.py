import json
from pathlib import Path

class ReportGenerator:
    """Formats and exports skill comparison gap analysis reports."""


    # ANSI color escape codes for terminal styling
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


    @classmethod
    def generate_terminal_report(cls, results: dict, use_color: bool = True) -> str:
        """Generates a structured, formatted report string for console display."""
        match_pct = results.get("match_percentage", 0.0)
        matched = results.get("matched_skills", [])
        missing = results.get("missing_skills", [])
        total = results.get("total_job_skills", 0)

        color_prefix = cls.GREEN if match_pct >= 70 else (cls.CYAN if match_pct >= 40 else cls.RED)
        c_reset = cls.RESET if use_color else ""
        c_bold = cls.BOLD if use_color else ""
        c_color = color_prefix if use_color else ""
        c_green = cls.GREEN if use_color else ""
        c_red = cls.RED if use_color else ""

        lines = [
            "=" * 56,
            f"{c_bold}  SKILL MATCH REPORT: {c_color}{match_pct}% Match{c_reset}",
            "=" * 56,
            f"Total In-Demand Skills Detected: {total}",
            "",
            f"{c_bold}[+] Matched Candidate Skills ({len(matched)}):{c_reset}",
        ]

        if matched:
            for skill in matched:
                lines.append(f"    {c_green}✓{c_reset} {skill}")
        else:
            lines.append("    (None)")

        lines.extend([
            "",
            f"{c_bold}[-] Missing Skills to Acquire ({len(missing)}):{c_reset}",
        ])

        if missing:
            for skill in missing:
                lines.append(f"    {c_red}✗{c_reset} {skill}")
        else:
            lines.append("    (None - Candidate meets all required skills!)")

        lines.append("=" * 56)
        return "\n".join(lines)

    @staticmethod
    def export_json(results: dict, output_path: str | Path) -> None:
        """Exports structured gap-analysis results to a JSON file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    @staticmethod
    def export_markdown(results: dict, output_path: str | Path) -> None:
        """Exports comparison results to a GitHub-flavored Markdown report."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)


        match_pct = results.get("match_percentage", 0.0)
        matched = results.get("matched_skills", [])
        missing = results.get("missing_skills", [])
        total = results.get("total_job_skills", 0)


        md_lines = [
            "# Skill Gap Analysis Report",
            f"**Match Rating:** {match_pct}%  ",
            f"**Total Required Skills Identified:** {total}  ",
            "",
            "## Matched Skills",
        ]


        if matched:
            for s in matched:
                md_lines.append(f"- [x] `{s}`")
        else:
            md_lines.append("- *No overlapping skills found.*")


        md_lines.extend([
            "",
            "## Missing Skills (Recommended Focus Areas)",
        ])


        if missing:
            for s in missing:
                md_lines.append(f"- [ ] `{s}`")
        else:
            md_lines.append("- *No missing skills.*")


        md_lines.extend([
            "",
            "---",
            "*Report generated automatically by tech-skill-matcher-cli.*",
        ])


        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")


