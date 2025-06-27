from models import SessionLocal, JobPost
from api.jobs.adzuna import get_all_adzuna_jobs
from api.jobs.remotive import get_remotive_jobs
from api.jobs.usajobs import get_usajobs_jobs, normalize_usajobs, deduplicate_usajobs
from utils.utils import normalize_job
from hashlib import sha256
from collections import Counter
import traceback

def fetch_and_store_jobs():
    session = SessionLocal()
    try:
        seen_hashes = set()
        unique_jobs = []

        # --- Fetch jobs from Adzuna ---
        adzuna_jobs = get_all_adzuna_jobs(pages=30)
        for job in adzuna_jobs:
            url = job.get("url")
            if not url:
                continue
            job_hash = sha256(url.encode()).hexdigest()
            if job_hash in seen_hashes:
                continue
            seen_hashes.add(job_hash)
            job["hash"] = job_hash
            unique_jobs.append(job)

        # --- Fetch jobs from USAJOBS ---
        raw_usajobs = get_usajobs_jobs(days_posted="30")
        print(f"[USAJOBS] Raw jobs fetched: {len(raw_usajobs)}")
        raw_usajobs = deduplicate_usajobs(raw_usajobs)
        normalized_usajobs = normalize_usajobs(raw_usajobs)
        print(f"[USAJOBS] After normalization {len(normalized_usajobs)}")

        for job in normalized_usajobs:
            url = job.get("url")
            if not url:
                continue
            job_hash = sha256(url.encode()).hexdigest()
            if job_hash in seen_hashes:
                continue
            seen_hashes.add(job_hash)
            job["hash"] = job_hash
            unique_jobs.append(job)

        # --- Fetch jobs from Remotive ---
        for job in get_remotive_jobs():
            url = job.get("url")
            if not url:
                continue
            job_hash = sha256(url.encode()).hexdigest()
            if job_hash in seen_hashes:
                continue
            seen_hashes.add(job_hash)
            job["hash"] = job_hash
            unique_jobs.append(job)

        print(f"[Fetch] Total unique jobs collected: {len(unique_jobs)}")

        # Optional: Print job counts by source
        source_counts = Counter(job["source"] for job in unique_jobs)
        print("[Sources] Job counts by source:", dict(source_counts))

        # --- Store in DB ---
        new_jobs = 0
        for job in unique_jobs:
            try:
                if session.query(JobPost).filter_by(hash=job["hash"]).first():
                    continue

                job = normalize_job(job)

                post = JobPost(
                    title=job["title"],
                    company=job["company"],
                    category=job["category"],
                    job_type=job["job_type"],
                    location=job["location"][:255],
                    salary=job.get("salary"),
                    created_at=job["created"],
                    url=job["url"],
                    source=job["source"],
                    tags=job["tags"],
                    hash=job["hash"]
                )


                session.add(post)
                new_jobs += 1

            except Exception as insert_error:
                print(f"[Insert Error] Skipped job: {job.get('title')} | Error: {insert_error}")

        session.commit()
        print(f"[Scheduler] Saved {new_jobs} new jobs.")

    except Exception as e:
        print(f"[Scheduler] Error: {e}")
        traceback.print_exc()

    finally:
        session.close()
