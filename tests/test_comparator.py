import pytest
from src.comparator import ProfileComparator

class TestProfileComaparator:
    def test_full_match(self):
        candidate_skills = ["python","djongo","postgresql"]
        job_skills ={"python","djongo","postgresql"}
        comparator = ProfileComparator(candidate_skills)
        result = comparator.analyze_match(job_skills)

        assert result["match_percentage"] == 100.0
        assert result["matched_skills"] == ["djongo","postgresql","python"]
        assert result["missing_skills"] == []
        assert result["total_job_skills"] == 3

    def test_partial_match(self):
        candidate_skills = ["python","docker"]
        job_skills ={"python","docker","kubernetes","aws"}
        comparator = ProfileComparator(candidate_skills)
        result = comparator.analyze_match(job_skills)
    
        assert result["match_percentage"] == 50.0
        assert sorted(result["matched_skills"]) == ["docker","python"]
        assert sorted(result["missing_skills"]) == ["aws","kubernetes"]
        assert result["total_job_skills"] == 4
                                    
    def test_zero_match(self):
        candidate_skills = ["java","spring"]
        job_skills ={"python","django"}
        comparator = ProfileComparator(candidate_skills)
        result = comparator.analyze_match(job_skills)

        assert result["match_percentage"] == 0.0
        assert result["matched_skills"] == []
        assert len(result["missing_skills"]) == 2 

    def test_empty_job_skills_no_division_by_zero(self):
        candidate_skills = ["python","sql"]
        comparator = ProfileComparator(candidate_skills)
        result = comparator.analyze_match(set())

        assert result["match_percentage"] == 0.0
        assert result["total_job_skills"] == 0