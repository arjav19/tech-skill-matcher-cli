import json
from pathlib import Path
import re




class SkillExtractor:
    """Extracts technical skills from raw text using compiled regex patterns."""


    def __init__(self, taxonomy_path: str | Path):
       self.taxonomy = self._load_taxonomy(taxonomy_path)
       self.compiled_patterns = self._compile_patterns()


    def _load_taxonomy(self, path: str | Path) -> dict:
       with open(path, "r", encoding="utf-8") as f:
         return json.load(f)


    def _compile_patterns(self) -> dict[str, list[re.Pattern]]:
       """Compiles regex patterns for each skill alias with word boundary protection."""
       compiled = {}
       for category, skills in self.taxonomy.items():
         for canonical_name, aliases in skills.items():
           patterns = []
           for alias in aliases:
             # Escape special characters like +, #, .
             escaped = re.escape(alias)
             # Enforce strict word boundaries
             pattern = re.compile(
                 rf"(?<!\w){escaped}(?!\w)",
                 re.IGNORECASE if len(alias) > 2 else 0,
             )
             patterns.append(pattern)
           compiled[canonical_name] = patterns
       return compiled


    def extract_skills(self, text: str) -> set[str]:
       """Returns a set of unique canonical skill names detected in the text."""
       detected_skills = set()
       for canonical_name, patterns in self.compiled_patterns.items():
         for pattern in patterns:
           if pattern.search(text):
             detected_skills.add(canonical_name)
             break  # Found this skill, move to next canonical skill
       return detected_skills
