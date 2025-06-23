from models import SessionLocal, JobPost
from jobs.adzuna import get_adzuna_jobs, normalize_adzuna_jobs
from hashlib import sha256
from datetime import datetime

def fetch_and_store_jobs():
    session = SessionLocal()
    try:
        raw_jobs = get_adzuna_jobs(results_per_page=50)
        jobs = normalize_adzuna_jobs(raw_jobs)
        new_jobs = 0


        for job in jobs:
            job_hash = sha256(job["url"].encode()).hexdigest()
            exists = session.query(JobPost).filter_by(hash=job_hash).first()
            if not exists:
                post = JobPost(
                    title=job["title"],
                    company=job["company"],
                    category=job["category"],
                    job_type=job["job_type"],
                    location=job["location"],
                    salary=job["salary"],
                    created_at=datetime.fromisoformat(job["created"]),
                    source=job["source"],
                    hash=job_hash
                )
                session.add(post)
                new_jobs += 1

        session.commit()
        print(f"[Scheduler] Saved {new_jobs} new jobs.")
    except:
        print(f"[Scheduler] Error: {e}")
    finally:
        session.close()