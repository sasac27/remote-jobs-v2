import requests
import os
from dotenv import load_dotenv
from utils.utils import extract_tags
from hashlib import sha256
from datetime import datetime
import time
from dateutil import parser as date_parser

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobFetcherBot/1.0)"
}

def get_all_adzuna_jobs(pages=3):
    """Fetch and normalize jobs from multiple Adzuna pages."""
    all_jobs = []
    for p in range(1, pages + 1):
        raw = get_adzuna_jobs(page=p, results_per_page=100)
        all_jobs.extend(raw)
        print(f"[Adzuna] ✅ Fetched {len(raw)} jobs from page {p}")
    return normalize_adzuna_jobs(all_jobs)


def get_adzuna_jobs(country="us", page=1, results_per_page=100, what=None, where=None, retries=3):
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
    params = {
        "app_id": os.getenv("ADZUNA_API_ID"),
        "app_key": os.getenv("ADZUNA_API_KEY"),
        "results_per_page": results_per_page,
        "content-type": "application/json",
        "sort_by": "date"
    }
    if what:
        params["what"] = what
    if where:
        params["where"] = where

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.RequestException as e:
            print(f"[Adzuna] ⚠️ Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return []


def clean_adzuna_salary(min_val, max_val, currency="USD", period="year"):
    try:
        if min_val and max_val:
            return f"{currency} {int(min_val):,} - {int(max_val):,} /{period}"
        elif min_val:
            return f"{currency} {int(min_val):,} /{period}"
        elif max_val:
            return f"{currency} {int(max_val):,} /{period}"
    except Exception as e:
        print(f"[Adzuna] Salary formatting error: {e}")
    return None


def normalize_adzuna_jobs(raw_jobs):
    jobs = []
    seen_urls = set()

    for job in raw_jobs:
        url = job.get("redirect_url")
        if not job.get("title") or not job.get("company") or not url or url in seen_urls:
            continue
        seen_urls.add(url)

        title = job.get("title", "").strip()
        description = job.get("description", "").strip()[:500]
        location = job.get("location", {}).get("display_name", "Unknown")

        # Extract tags
        tags = extract_tags(f"{title}. {description}")
        if "remote" in location.lower():
            tags.append("remote")
        tags = sorted(set(t.lower() for t in tags if t))

        # Parse date safely

        created_raw = job.get("created")
        try:
            created_dt = date_parser.parse(created_raw) if created_raw else datetime.utcnow()
        except Exception:
            created_dt = datetime.utcnow()

        created = created_dt.isoformat()

        # Salary
        salary = clean_adzuna_salary(
            job.get("salary_min"),
            job.get("salary_max"),
            job.get("salary_currency") or "USD",
            job.get("salary_period") or "year"
        )

        jobs.append({
            "title": title,
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "url": url,
            "category": job.get("category", {}).get("label", "Uncategorized"),
            "job_type": job.get("contract_time", "Unknown"),
            "location": location,
            "description": description,
            "created": created,
            "salary": salary or "Not specified",
            "tags": tags,
            "source": "adzuna",
            "hash": sha256(url.encode()).hexdigest()
        })

    return jobs
