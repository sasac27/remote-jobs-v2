import requests
from datetime import datetime
from dateutil.parser import parse as parse_date

def normalize_location(raw_location):
    if not raw_location or "anywhere" in raw_location.lower():
        return "Remote"
    return raw_location.strip()

def extract_tags(title, description):
    keywords = [
        "python", "javascript", "react", "node", "flask", "django", "aws", "docker",
        "sql", "typescript", "java", "ruby", "go", "kubernetes", "linux", "graphql"
    ]
    combined_text = f"{title.lower()} {description.lower()}"
    return [kw for kw in keywords if kw in combined_text]

def normalize_salary(raw_salary):
    if not raw_salary or "n/a" in raw_salary.lower():
        return "Unknown"
    return raw_salary.strip()

def get_data():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get("https://remotive.com/api/remote-jobs", headers=headers)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for job in data["jobs"]:
            description = job.get("description", "").strip()[:300]
            title = job["title"]
            tags = job.get("tags") or extract_tags(title, description)

            created = job.get("publication_date")
            created_date = parse_date(created) if created else datetime.utcnow()

            jobs.append({
                "title": title,
                "company": job["company_name"],
                "url": job["url"],
                "category": job["category"],
                "job_type": job["job_type"],
                "location": normalize_location(job["candidate_required_location"]),
                "tags": tags,
                "skills": tags,  # alias for clarity
                "salary": normalize_salary(job.get("salary")),
                "created": created_date.isoformat(),
                "description": description,
                "source": "remotive"
            })

        return jobs

    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []
