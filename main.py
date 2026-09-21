import argparse
import json
import sys
from src.comparator import ProfileComparator
from src.extractor import SkillExtractor
from src.parser import JobParser, RemoteJobParser

def main():
    parser =  argparse.ArgumentParser(
        description= "Tech Job and Skill Matcher CLI"
    )
    parser.add_argument("--file",help="Path to local job description file")
    parser.add_argument("--url",help="URL to remote job description")
    parser.add_argument(
        "--profile", default="data/candidate_profile.json",
        help= "Path to candidate profile",
        )
    parser.add_argument(
            "--taxonomy", 
            default="data/skill_taxonomy.json",
            help= "Path to skills taxonomy",
            )
    parser.add_argument(
        "--json",action="store_true",help="Output as raw JSON"
        )
    args = parser.parse_args()

    if not args.file and not args.url:
        print("Error: Please provide either --file or --url",file=sys.stderr)
        sys.exit(1)

    # 1. Parse text    
    if args.file:
        raw_text = JobParser.parse_file(args.file)
    else:
        raw_text = RemoteJobParser.fetch_from_url(args.url)

    # 2. Extract Skills
    extractor  = SkillExtractor(args.taxonomy)
    job_skills = extractor.extract_skills(raw_text)

    # 3. Load profile & compare 
    with open(args.profile,"r") as f:
        profile_data = json.load(f)
    candidate_skills = profile_data.get("slills",[]) 

    comparator = ProfileComparator(candidate_skills)
    results = comparator.analyze_match(job_skills)

    # 4. Output results
    if args.json:
        print(json.dumps(results,indent=2))
    else:
        print("\n" + "=" * 50)
        print(f"  SKILL MATCH REPORT: {results['match_percentage']}% Match")
        print("=" * 50)
        print(f"Total Required Skills Detected: {results['total_job_skills']}")
        print(f"\n[+] Matched Skills ({len(results['matched_skills'])}):")
        for s in results["matched_skills"]:
            print(f" ✓ {s}")
        print(f"\n[-] Missing Skills to Learn ({len(results['missing_skills'])}):")
        for s in results["missing_skills"]:
            print(f"   ✗ {s}") 
        print("=" * 50 + "\n")

if __name__ == "__main__":
    main()