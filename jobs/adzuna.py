import requests
from datetime import datetime
from dateutil.parser import parse as parse_date

def normalize_location(location):
    if not location:
        return "Unknown"
    return location.strip()

def normalize_salary(salary_min, salary_max, currency):
    if not salary_min and not salary_max:
        return "Unknown"
    if salary_min and salary_max:
        return f"{currency} {int(salary_min)} - {int(salary_max)}"
    return f"{currency} {int(salary_min or salary_max)}"

def extract_tags(title, description):
    keywords = [
        "python", "javascript", "react", "node", "flask", "django", "aws", "docker",
        "sql", "typescript", "java", "ruby", "go", "kubernetes", "linux", "graphql"
    ]
    combined_text = f"{title.lower()} {description.lower()}"
    return [kw for kw in keywords if kw in combined_text]

def get_adzuna_jobs(country="us", page=1, results_per_page=20, what=None, where=None):
    import os
    from dotenv import load_dotenv
    load_dotenv()

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
    params = {
        "app_id": os.getenv("ADZUNA_API_ID"),
        "app_key": os.getenv("ADZUNA_API_KEY"),
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }
    if what:
        params["what"] = what
    if where:
        params["where"] = where

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"Adzuna API error: {e}")
        return []

def normalize_adzuna_jobs(raw_jobs):
    jobs = []
    for job in raw_jobs:
        title = job.get("title", "Untitled")
        description = job.get("description", "")[:300]
        created = job.get("created")
        created_date = parse_date(created) if created else datetime.utcnow()
        tags = extract_tags(title, description)


        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        if salary_min and salary_max:
            salary_num = round((salary_min + salary_max) / 2, 2)
        elif salary_min:
            salary_num = salary_min
        elif salary_max:
            salary_num = salary_max
        else:
            salary_num = None

        jobs.append({
            "title": title,
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "url": job.get("redirect_url"),
            "category": job.get("category", {}).get("label", "Uncategorized"),
            "job_type": job.get("contract_time", "Unknown"),
            "location": normalize_location(job.get("location", {}).get("display_name")),
            "tags": tags,
            "skills": tags,
            "salary": normalize_salary(job.get("salary_min"), job.get("salary_max"), job.get("salary_currency", "$")),
            "salary_num": salary_num, 
            "created": created_date.isoformat(),
            "description": description,
            "source": "adzuna"
        })
    return jobs
