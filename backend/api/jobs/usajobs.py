import requests
from datetime import datetime
from dateutil.parser import parse as parse_date
from backend.utils.utils import extract_tags
from hashlib import sha256
import time
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://data.usajobs.gov/api/search"
HEADERS = {
    "Host": "data.usajobs.gov",
    "User-Agent": os.getenv("USAJOBS_USER_AGENT"),
    "Authorization-Key": os.getenv("USAJOBS_API_KEY")
    
}

BROAD_KEYWORDS = [
    "", "tech", "IT", "data", "software", "developer", "engineer", "scientist",
    "analyst", "cyber", "support", "computer", "network", "security", "systems"
]

BROAD_LOCATIONS = [
    "", "Remote", "United States", "California", "Texas", "Virginia", "Colorado",
    "New York", "Florida", "Georgia", "Illinois", "Washington DC", "North Carolina", "Massachusetts"
]

CATEGORY_CODES = []  # Optional filter e.g., ["0300", "0500"]

RATE_MAP = {
    "PA": "year",
    "PH": "hour",
    "PM": "month",
    "PD": "day"
}


def get_usajobs_jobs(days_posted="30", results_per_page=25, max_pages=10):
    all_jobs = []

    for keyword in BROAD_KEYWORDS:
        for location in BROAD_LOCATIONS:
            page = 1
            while page <= max_pages:
                params = {
                    "Keyword": keyword,
                    "LocationName": location,
                    "Page": page,
                    "ResultsPerPage": results_per_page,
                    "DatePosted": days_posted,
                }
                if CATEGORY_CODES:
                    params["JobCategoryCode"] = ",".join(CATEGORY_CODES)

                try:
                    response = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    items = data.get("SearchResult", {}).get("SearchResultItems", [])
                    if not items:
                        break

                    all_jobs.extend(items)

                    has_more = data.get("SearchResult", {}).get("UserArea", {}).get("HasMore", False)
                    if not has_more:
                        break
                    page += 1

                except requests.RequestException as e:
                    print(f"[USAJOBS] ⚠️ Error on page {page} ({keyword}, {location}): {e}")
                    break
                time.sleep(0.4)  # Respect rate limiting

    return all_jobs


def normalize_usajobs(raw_jobs):
    jobs = []
    for item in raw_jobs:
        desc = item.get("MatchedObjectDescriptor", {})
        if not desc:
            continue

        title = desc.get("PositionTitle", "Untitled Job").strip()
        company = desc.get("OrganizationName", "USA Government").strip()
        description = desc.get("UserArea", {}).get("Details", {}).get("JobSummary", "No description.").strip()

        location_list = desc.get("PositionLocation", [])
        locations = ", ".join(loc.get("LocationName", "N/A") for loc in location_list[:5]) or "Unknown"
        if len(location_list) > 5:
            locations += ", and more"

        # Tags
        tags = extract_tags(f"{title}. {description}")
        if "remote" in locations.lower():
            tags.append("remote")
        tags = sorted(set(t.lower() for t in tags if t))

        # Date
        pub_date = desc.get("PublicationDate")
        try:
            created = parse_date(pub_date) if pub_date else datetime.utcnow()
        except Exception:
            created = datetime.utcnow()

        # Salary
        salary_data = desc.get("PositionRemuneration") or []
        if salary_data:
            try:
                s = salary_data[0]
                min_val = float(s.get("MinimumRange", 0))
                max_val = float(s.get("MaximumRange", 0))
                unit = f"/{RATE_MAP.get(s.get('RateIntervalCode', '').strip(), 'year')}"
                if min_val and max_val:
                    salary = f"${int(min_val):,} - ${int(max_val):,}{unit}"
                elif min_val:
                    salary = f"${int(min_val):,}{unit}"
                else:
                    salary = "Not specified"
            except Exception:
                salary = "Not specified"
        else:
            salary = "Not specified"

        # URL
        url = desc.get("PositionURI", "").strip()
        if not url:
            fallback_key = f"{title}_{company}"
            url = f"https://usajobs.gov/fallback/{sha256(fallback_key.encode()).hexdigest()}"

        jobs.append({
            "title": title,
            "company": company,
            "category": (desc.get("JobCategory") or [{}])[0].get("Name", "Government").strip(),
            "job_type": (desc.get("PositionSchedule") or [{}])[0].get("Name", "Unknown").strip(),
            "location": locations,
            "salary": salary,
            "created": created.isoformat(),
            "source": "usajobs",
            "url": url,
            "hash": sha256(url.encode()).hexdigest(),
            "tags": tags,
            "description": description[:500]
        })

    print(f"[USAJOBS] ✅ Normalized {len(jobs)} jobs")
    return jobs


def deduplicate_usajobs(raw_jobs):
    seen = set()
    unique = []

    for job in raw_jobs:
        desc = job.get("MatchedObjectDescriptor", {})
        if not desc:
            continue

        url = desc.get("PositionURI", "").strip()
        if not url:
            fallback_key = f"{desc.get('PositionTitle', '')}_{desc.get('OrganizationName', '')}".strip()
            url = f"https://usajobs.gov/fallback/{sha256(fallback_key.encode()).hexdigest()}"

        if url not in seen:
            seen.add(url)
            unique.append(job)

    print(f"[USAJOBS] 🧹 Deduplicated to {len(unique)} jobs")
    return unique
