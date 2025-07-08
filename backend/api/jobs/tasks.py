from backend.models import SessionLocal, JobPost
from backend.api.jobs.adzuna import get_all_adzuna_jobs
from backend.api.jobs.remotive import get_remotive_jobs
from backend.api.jobs.usajobs import get_usajobs_jobs, normalize_usajobs, deduplicate_usajobs
from backend.utils.utils import normalize_job
from backend.utils.job_hash import generate_job_hash
from collections import Counter
import traceback
from datetime import datetime

def fetch_and_store_jobs():
    session = SessionLocal()
    try:
        seen_hashes = set(h[0] for h in session.query(JobPost.hash).all())
        unique_jobs = []

        # --- Fetch jobs from Adzuna ---
        adzuna_jobs = get_all_adzuna_jobs(pages=30)
        for job in adzuna_jobs:
            if not job.get("title") or not job.get("company"):
                continue
            created = job.get("created") or datetime.utcnow().isoformat()
            job_hash = generate_job_hash(job["title"], job["company"], created)
            if job_hash in seen_hashes:
                continue
            seen_hashes.add(job_hash)
            job["hash"] = job_hash
            job["created"] = created
            unique_jobs.append(job)

        # --- Fetch jobs from USAJOBS ---
        raw_usajobs = get_usajobs_jobs(days_posted="30")
        print(f"[USAJOBS] Raw jobs fetched: {len(raw_usajobs)}")
        raw_usajobs = deduplicate_usajobs(raw_usajobs)
        normalized_usajobs = normalize_usajobs(raw_usajobs)
        print(f"[USAJOBS] After normalization: {len(normalized_usajobs)}")

        for job in normalized_usajobs:
            if not job.get("title") or not job.get("company"):
                continue
            created = job.get("created") or datetime.utcnow().isoformat()
            job_hash = generate_job_hash(job["title"], job["company"], created)
            if job_hash in seen_hashes:
                continue
            seen_hashes.add(job_hash)
            job["hash"] = job_hash
            job["created"] = created
            unique_jobs.append(job)

        # --- Fetch jobs from Remotive ---
        remotive_jobs = get_remotive_jobs()
        for job in remotive_jobs:
            if not job.get("title") or not job.get("company"):
                continue
            created = job.get("created") or datetime.utcnow().isoformat()
            job_hash = generate_job_hash(job["title"], job["company"], created)
            if job_hash in seen_hashes:
                continue
            seen_hashes.add(job_hash)
            job["hash"] = job_hash
            job["created"] = created
            unique_jobs.append(job)

        print(f"[Fetch] Total unique jobs collected: {len(unique_jobs)}")


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
                    category=job.get("category"),
                    job_type=job.get("job_type"),
                    location=(job.get("location") or "")[:255],
                    salary=job.get("salary"),
                    created_at=job["created"],
                    url=job.get("url"),
                    source=job.get("source"),
                    tags=job.get("tags"),
                    hash=job["hash"]
                )

                session.add(post)
                new_jobs += 1

            except Exception as insert_error:
                print(f"[Insert Error] Skipped job: {job.get('title')} | Error: {insert_error}")

        session.commit()
        print(f"[Store] Saved {new_jobs} new jobs.")

    except Exception as e:
        print(f"[Fetch Error] {e}")
        traceback.print_exc()

    finally:
        session.close()
