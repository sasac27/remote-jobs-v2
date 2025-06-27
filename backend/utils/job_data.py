# utils/job_data.py

from models import SessionLocal, JobPost

def get_all_jobs():
    session = SessionLocal()
    jobs = session.query(JobPost).all()
    result = []
    for job in jobs:
        result.append({
            "title": job.title,
            "company": job.company,
            "category": job.category or "Unknown",
            "job_type": job.job_type or "Unknown",
            "location": job.location or "Unknown",
            "salary": job.salary or "Not specified",
            "created": job.created_at.isoformat() if job.created_at else "",
            "source": job.source or "Unknown",
            "tags": job.tags or [],
            "hash": job.hash,
            # Optional: Extract salary_num from salary string if not in DB
        })
    session.close()
    return result
