class ProfileComparator:
     """Compares extracted job skills against candidate profile."""


     def __init__(self, candidate_skills: list[str] | set[str]):
       self.candidate_skills = {s.lower() for s in candidate_skills}


     def analyze_match(self, job_skills: set[str]) -> dict:
       if not job_skills:
         return {
             "match_percentage": 0.0,
             "matched_skills": [],
             "missing_skills": [],
             "total_job_skills": 0,
         }


       matched = sorted(list(self.candidate_skills.intersection(job_skills)))
       missing = sorted(list(job_skills.difference(self.candidate_skills)))
       match_percentage = round((len(matched) / len(job_skills)) * 100, 1)


       return {
           "match_percentage": match_percentage,
           "matched_skills": matched,
           "missing_skills": missing,
           "total_job_skills": len(job_skills),
       }
