from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from backend.models import SessionLocal, JobPost
from sqlalchemy import func
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import numpy as np
import re


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")

@dashboard_bp.route("/dashboard")
@jwt_required()
def dashboard():
    user_email = get_jwt_identity()
    session = SessionLocal()

    try:
        total_jobs = session.query(func.count(JobPost.id)).scalar()

        # Top categories, locations, sources, companies
        top_categories = session.query(JobPost.category, func.count()).group_by(JobPost.category).order_by(func.count().desc()).limit(5).all()
        top_locations = session.query(JobPost.location, func.count()).group_by(JobPost.location).order_by(func.count().desc()).limit(5).all()
        top_sources = session.query(JobPost.source, func.count()).group_by(JobPost.source).order_by(func.count().desc()).limit(5).all()
        top_companies = session.query(JobPost.company, func.count()).group_by(JobPost.company).order_by(func.count().desc()).limit(5).all()

        # Job type distribution
        job_type_dist = session.query(JobPost.job_type, func.count()).group_by(JobPost.job_type).all()

        # Top tags
        EXCLUDED_JOB_TYPE_TAGS = {
        "Full-time", "Part-time", "Flexible", "Seasonal", "Shift", "Other", "Contract", "Internship", "Remote", "Temporary"
        }

        tags_counter = Counter()
        for job in session.query(JobPost.tags).filter(JobPost.tags.isnot(None)):
            tags = [
                t.strip().lower() for t in (job.tags or [])
                if isinstance(t, str) and t.strip() and t.strip().lower() not in EXCLUDED_JOB_TYPE_TAGS
            ]
        tags_counter.update(tags)

        top_tags = tags_counter.most_common(10)

        raw_salaries = session.query(JobPost.salary).filter(JobPost.salary != None).all()
        salaries = [extract_numeric_salary(j.salary) for j in raw_salaries if extract_numeric_salary(j.salary) is not None]

        salary_coverage = round((len(salaries) / total_jobs) * 100, 1) if total_jobs else 0
        avg_salary = round(np.mean(salaries), 2) if salaries else 0
        salary_histogram = {"bin_edges": [], "counts": []}
        if salaries:
            counts, bin_edges = np.histogram(salaries, bins=8)
            salary_histogram = {
                "bin_edges": [round(b, 2) for b in bin_edges],
                "counts": counts.tolist()
            }

        # Job posting trend (per day)
        trend_counter = Counter()
        jobs = session.query(JobPost.created_at).all()
        for (created_at,) in jobs:
            if created_at:
                trend_counter[created_at.date()] += 1
        trend_data = sorted(trend_counter.items())
        trend_labels = [d.strftime("%Y-%m-%d") for d, _ in trend_data]
        trend_values = [count for _, count in trend_data]

        # Recent activity
        today = datetime.utcnow().date()
        jobs_this_week = sum(count for date, count in trend_data if date >= today - timedelta(days=7))
        jobs_this_month = sum(count for date, count in trend_data if date >= today - timedelta(days=30))

        return jsonify({
            "user": user_email,
            "total_jobs": total_jobs,
            "average_salary": avg_salary,
            "salary_coverage": salary_coverage,
            "salary_histogram": salary_histogram,
            "trend_labels": trend_labels,
            "trend_values": trend_values,
            "top_categories": [{"label": c, "count": n} for c, n in top_categories],
            "top_locations": [{"label": l, "count": n} for l, n in top_locations],
            "top_sources": [{"label": s, "count": n} for s, n in top_sources],
            "top_companies": [{"label": c, "count": n} for c, n in top_companies],
            "job_type_distribution": [{"label": jt, "count": n} for jt, n in job_type_dist],
            "top_tags": [{"label": tag, "count": count} for tag, count in top_tags],
            "jobs_this_week": jobs_this_week,
            "jobs_this_month": jobs_this_month
        })

    finally:
        session.close()



def extract_numeric_salary(salary_str):
    """Extract the first numeric value from a salary string like '$50k - $70k'"""
    if not salary_str:
        return None
    salary_str = salary_str.replace(",", "")
    match = re.search(r"\$?(\d+(?:\.\d+)?)", salary_str)
    if match:
        return float(match.group(1))
    return None

