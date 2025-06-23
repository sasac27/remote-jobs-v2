from models import SessionLocal, JobPost
from jobs.remotive import get_data as get_remotive_data
from jobs.adzuna import get_adzuna_jobs, normalize_adzuna_jobs
from utils.job_hash import generate_job_hash
from datetime import datetime

def fetch_and_store_jobs():
    session = SessionLocal()

    all_jobs = []

    #Remotive jobs
    remotive_jobs = get_remotive_data()
    for job in remotive_jobs:
        job_hash = generate_job_hash(job["title"], job["company"], job["created"])
        if not session.query(JobPost).filter_by(hash=job_hash).first():
            all_jobs.append(JobPost(
                title=job["title"],
                company=job["company"],
                category=job["category"],
                job_type=job["job_type"],
                location=job["location"],
                salary=job["salary"],
                created_at=datetime.fromisoformat(job["created"]),
                source="remotive",
                hash=job_hash
            ))

    raw_adzuna = get_adzuna_jobs(results_per_page=50)
    adzuna_jobs = normalize_adzuna_jobs(raw_adzuna)
    for job in adzuna_jobs:
        job_hash = generate_job_hash(job["title"], job["company"], job["created"])
        if not session.query(JobPost).filter_by(hash=job_hash).first():
            all_jobs.append(JobPost(
                title=job["title"],
                company=job["company"],
                category=job["category"],
                job_type=job["job_type"],
                location=job["location"],
                salary=job["salary"],
                created_at=datetime.fromisoformat(job["created"]),
                source="adzuna",
                hash=job_hash
            ))

    #bulk insert
    if all_jobs:
        session.add_all(all_jobs)
        session.commit()
        print(f"Saved {len(all_jobs)} new jobs.")
    else:
        print("No new jobs to add.")

    session.close()

if __name__ == "__main__":
    fetch_and_store_jobs()