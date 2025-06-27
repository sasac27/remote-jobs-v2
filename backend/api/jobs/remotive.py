import requests
from datetime import datetime
from dateutil.parser import parse as parse_date
from utils.utils import extract_tags
from hashlib import sha256
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def normalize_location(raw_location):
    if not raw_location or "anywhere" in raw_location.lower():
        return "Remote"
    return raw_location.strip()

def clean_remotive_salary(raw_salary):
    """Attempt to normalize Remotive salary to a clean string."""
    if not raw_salary:
        return "Not specified"

    try:
        parts = raw_salary.replace("USD", "").replace("usd", "").replace("$", "").split("-")
        parts = [int(p.strip().replace(",", "")) for p in parts if p.strip().replace(",", "").isdigit()]
        if len(parts) == 2:
            return f"${parts[0]:,} - ${parts[1]:,}/year"
        elif len(parts) == 1:
            return f"${parts[0]:,}/year"
    except Exception:
        pass

    return raw_salary.strip()

def fetch_remotive_data(retries=3, delay=2):
    url = "https://remotive.io/api/remote-jobs"

    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=delay,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://remotive.io"
    }

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[Remotive] ❌ Failed to fetch jobs: {e}")
        return {}
    
    
def get_remotive_jobs():
    data = fetch_remotive_data()
    jobs = []
    seen_urls = set()

    for job in data.get("jobs", []):
        title = job.get("title", "").strip()
        company = job.get("company_name", "").strip()
        url = job.get("url", "").strip()
        description = job.get("description", "").strip()

        if not title or not company or not url or url in seen_urls:
            continue
        seen_urls.add(url)

        # Tags
        tags = job.get("tags") or extract_tags(f"{title}. {description}")
        tags = sorted(set(tag.lower() for tag in tags if tag))

        # Date
        created_str = job.get("publication_date")
        try:
            created = parse_date(created_str) if created_str else datetime.utcnow()
        except Exception:
            created = datetime.utcnow()

        # Salary
        salary = clean_remotive_salary(job.get("salary", "").strip())

        jobs.append({
            "title": title,
            "company": company,
            "url": url,
            "category": job.get("category", "Uncategorized"),
            "job_type": job.get("job_type", "Unknown"),
            "location": normalize_location(job.get("candidate_required_location")),
            "tags": tags,
            "salary": salary,
            "created": created.isoformat(),
            "description": description[:500],
            "source": "remotive",
            "hash": sha256(url.encode()).hexdigest()
        })

    print(f"[Remotive] ✅ Normalized {len(jobs)} jobs")
    return jobs
