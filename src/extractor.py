import json
from pathlib import Path
import re
from typing import Union


class SkillExtractor:
    """Extracts predefined technical skills from text using regular expressions and aliases."""

    def __init__(self, taxonomy_path: Union[str, Path]) -> None:
        """
        Initialize the extractor with a path to the taxonomy JSON file.
        Supports both flat taxonomy dictionaries and categorized/nested taxonomy dictionaries.
        """
        self.taxonomy_path = Path(taxonomy_path)
        self.taxonomy: dict[str, list[str]] = self._load_taxonomy(self.taxonomy_path)
        self.patterns: dict[str, list[re.Pattern]] = self._compile_patterns()

    def _load_taxonomy(self, taxonomy_path: Path) -> dict[str, list[str]]:
        """
        Loads the taxonomy JSON file and flattens nested category dictionaries.
        Ensures keys and aliases are normalized to lowercase strings.
        """
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        flattened: dict[str, list[str]] = {}

        for key, value in raw_data.items():
            if isinstance(value, dict):
                # Nested category, e.g. "languages": {"python": ["py", "python3"], "c": ["c"]}
                for skill_name, aliases in value.items():
                    flattened[str(skill_name).lower()] = [
                        str(a).lower() for a in aliases
                    ]
            elif isinstance(value, list):
                # Flat mapping, e.g. "python": ["python", "py"]
                flattened[str(key).lower()] = [str(a).lower() for a in value]

        return flattened

    def _compile_patterns(self) -> dict[str, list[re.Pattern]]:
        """
        Compiles regular expression patterns for each skill and its aliases.
        Uses boundaries (?<!\\w) and (?!\\w) to support special characters (like C++, C#).
        Allows both uppercase and lowercase matches for short aliases (e.g. C, Go).
        """
        compiled: dict[str, list[re.Pattern]] = {}

        for skill, aliases in self.taxonomy.items():
            pattern_list: list[re.Pattern] = []
            for alias in aliases:
                escaped = re.escape(alias)
                # For 1-2 character tokens (like 'c', 'r', 'go'), allow case variations
                if len(alias) <= 2:
                    pattern = re.compile(
                        rf"(?<!\w)(?:{escaped}|{re.escape(alias.upper())})(?!\w)"
                    )
                else:
                    pattern = re.compile(
                        rf"(?<!\w){escaped}(?!\w)",
                        re.IGNORECASE,
                    )
                pattern_list.append(pattern)
            compiled[skill] = pattern_list

        return compiled

    def extract_skills(self, text: str) -> set[str]:
        """
        Scans input text and returns a set of canonical matched skill keys.
        """
        if not text or not isinstance(text, str):
            return set()

        matched_skills: set[str] = set()

        for skill, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    matched_skills.add(skill)
                    break  # Found match for this skill, no need to check other aliases

        return matched_skills

