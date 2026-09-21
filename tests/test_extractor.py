import json
import pytest
from src.extractor import SkillExtractor

@pytest.fixture
def sample_taxanomy(tmp_path):
    """Creates a temprary taxanomy JSON file for isolated testing"""
    taxanomy_data = {
        

      "languages": {
          "python": ["python", "python3", "py"],
          "c": ["c"],
          "c++": ["c++", "cpp"],
          "go": ["golang", "go"],
          "sql": ["sql"],
      },
      "frameworks": {
          "django": ["django"],
          "django_rest_framework": ["drf", "django rest framework"],
          "fastapi": ["fastapi"],
      },
      "databases": {"postgresql": ["postgresql", "postgres", "psql"]},

    }
    tax_file = tmp_path/"test_taxonomy.json"
    with open(tax_file,"w",encoding="utf-8") as f:
        json.dump(taxanomy_data,f)
    return tax_file

class TestSkillExtractor:

    def test_extractor_basic_skills(self,sample_taxonomy):
        extractor = SkillExtractor(sample_taxonomy)
        text = "We are hiring a Python developer with strong PostgreSQL skills."
        skills = extractor.extract_skills(text)

        assert "python" in skills
        assert "postgresql" in skills
        assert len(skills)  == 2

    def test_allias_resolution(self, sample_taxonomy):
        extractor = SkillExtractor(sample_taxonomy)
        text = "Must have experience with DRF and Postgres."
        skills = extractor.extract_skills(text)

        # Aliases should resolve to canonical taxonomy keys
        assert "django_rest_framework" in skills
        assert "postgresql" in skills

    def test_special_characters_cpp(self,sample_taxonomy):
        extractor = SkillExtractor(sample_taxonomy)
        text = "Experience with C++ and SQL is required."
        skills = extractor.extract_skills (text)

        assert "c++" in skills
        assert "sql" in skills

    def test_no_false_positive_on_single_letter_c(self, sample_taxonomy):
        extractor = SkillExtractor(sample_taxonomy)
        # Words containing 'c' should NOT trigger the programming language 'c'
        text = "Join our company for a great career in cloud computing."
        skills = extractor.extract_skills(text)

        assert "c" not in skills
        assert len(skills)==0

    def test_exact_single_letter_c_matches(self,sample_taxanomy):
        extractor = SkillExtractor(sample_taxanomy)
        text = "Strong proficiency in C and Python programming."
        skills = extractor.extract_skills(text)

        assert "c" in skills
        assert "python" in skills

    def test_empty_text(self,sample_taxanomy):
        extractor = SkillExtractor(sample_taxanomy)
        assert extractor.extract_skills("") == set()
        assert(
                extractor.extract_skills("No technical terms listed here.") == set()
                )
   


 
    