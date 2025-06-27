import re
from datetime import datetime
import yake  
# --------------------------
# Keyword Extraction with YAKE
# --------------------------
def extract_tags(text, max_tags=10):
    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=1,               # 1-gram keywords
        top=max_tags,
        dedupLim=0.9,      # remove near-duplicates
        features=None
    )
    keywords = kw_extractor.extract_keywords(text)
    tags = [kw.strip().lower() for kw, _ in keywords if 2 <= len(kw) <= 30]
    return sorted(set(tags))


# --------------------------
# Normalize Job
# --------------------------
def normalize_job(job):
    def safe_get(val, default="Unknown"):
        return val.strip() if isinstance(val, str) and val.strip() else default

    # Simplify job types
    raw_type = safe_get(job.get("job_type"), "Unknown").lower()
    if any(kw in raw_type for kw in ["full", "40", "35", "mon", "week"]):
        job_type = "Full-time"
    elif "part" in raw_type:
        job_type = "Part-time"
    elif "flex" in raw_type:
        job_type = "Flexible"
    elif "season" in raw_type:
        job_type = "Seasonal"
    elif "shift" in raw_type or "hour" in raw_type:
        job_type = "Shift"
    else:
        job_type = "Other"

    job["job_type"] = job_type
    job["title"] = safe_get(job.get("title"), "Untitled Job")
    job["company"] = safe_get(job.get("company"), "Unknown Company")
    job["category"] = safe_get(job.get("category"), "Uncategorized")
    job["location"] = safe_get(job.get("location"), "Unknown")
    job["salary"] = safe_get(job.get("salary"), "Not specified")
    job["tags"] = job.get("tags") or ["general"]

    # Normalize date field
    try:
        dt = job["created"]
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        elif not isinstance(dt, datetime):
            raise ValueError("Invalid datetime")
    except Exception:
        dt = datetime.utcnow()
    job["created"] = dt.isoformat()

    return job


# --------------------------
# Parse Salary Range
# --------------------------
def parse_salary_range(salary_str):
    if not salary_str:
        return None, None, None
    try:
        numbers = [int(n.replace(",", "")) for n in re.findall(r"\$?\b(\d{2,7})\b", salary_str)]
        if len(numbers) == 2:
            return numbers[0], numbers[1], (numbers[0] + numbers[1]) / 2
        elif len(numbers) == 1:
            return numbers[0], numbers[0], numbers[0]
    except Exception as e:
        print(f"[ERROR] Salary parse failed for: {salary_str} ({e})")
    return None, None, None
