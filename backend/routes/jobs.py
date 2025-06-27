# routes/jobs.py

from flask import Blueprint, request, jsonify
from models import SessionLocal, JobPost
from sqlalchemy import func
from sqlalchemy import or_, and_
import math
from datetime import datetime, timedelta

jobs_bp = Blueprint("api", __name__, url_prefix="/api")

@jobs_bp.route("/jobs", methods=["GET"])
def api_get_jobs():
    session = SessionLocal()
    try:
        # --- Query Params ---
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))

        source = request.args.get("source")
        category = request.args.get("category")
        location = request.args.get("location")
        keyword = request.args.get("keyword")
        job_type = request.args.get("job_type")
        tags = request.args.get("tags")  # comma-separated
        salary_min = request.args.get("salary_min", type=int)
        salary_max = request.args.get("salary_max", type=int)
        days_posted = request.args.get("days_posted", type=int)  # e.g. 7 = last week
        sort_by = request.args.get("sort_by", "created")  # or 'salary'
        sort_order = request.args.get("sort_order", "desc")  # 'asc' or 'desc'

        # --- Build Query ---
        query = session.query(JobPost)

        if source:
            query = query.filter(func.lower(JobPost.source) == source.lower())
        if category:
            query = query.filter(JobPost.category.ilike(f"%{category}%"))
        if location:
            query = query.filter(JobPost.location.ilike(f"%{location}%"))
        if keyword:
            query = query.filter(or_(
                JobPost.title.ilike(f"%{keyword}%"),
                JobPost.company.ilike(f"%{keyword}%"),
                JobPost.tags.ilike(f"%{keyword}%")
            ))
        if job_type:
            query = query.filter(JobPost.job_type.ilike(f"%{job_type}%"))
        if tags:
            for tag in tags.split(","):
                query = query.filter(JobPost.tags.ilike(f"%{tag.strip()}%"))
        if salary_min is not None:
            query = query.filter(JobPost.salary >= salary_min)
        if salary_max is not None:
            query = query.filter(JobPost.salary <= salary_max)
        if days_posted:
            cutoff = datetime.utcnow() - timedelta(days=days_posted)
            query = query.filter(JobPost.created_at >= cutoff)

        # --- Sort ---
        if sort_by == "salary":
            sort_col = JobPost.salary
        else:
            sort_col = JobPost.created_at

        sort_col = sort_col.asc() if sort_order == "asc" else sort_col.desc()

        # --- Execute ---
        total = query.count()
        jobs = query.order_by(sort_col).offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            "jobs": [job.to_dict() for job in jobs],
            "total": total,
            "page": page,
            "total_pages": math.ceil(total / per_page)
        })

    finally:
        session.close()
