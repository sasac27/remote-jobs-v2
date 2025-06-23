# routes/jobs.py

from flask import Blueprint, render_template, request, url_for, redirect
import math
from jobs.remotive import get_data
from jobs.adzuna import get_adzuna_jobs, normalize_adzuna_jobs

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/")
def home():
    return redirect(url_for("jobs.paginated_jobs_route"))

@jobs_bp.route("/jobs")
def paginated_jobs_route():
    source = request.args.get("source", "adzuna")
    return paginated_jobs(source)

def paginated_jobs(source):
    page = int(request.args.get("page", 1))
    per_page = 50
    category = request.args.get("category")
    location = request.args.get("location")
    keyword = request.args.get("keyword")

    if source == "remotive":
        jobs = get_data()
        if category:
            jobs = [job for job in jobs if category.lower() in job["category"].lower()]
        if location:
            jobs = [job for job in jobs if location.lower() in job["location"].lower()]
        if keyword:
            jobs = [job for job in jobs if keyword.lower() in job["title"].lower() or keyword.lower() in job["description"].lower()]
    elif source == "adzuna":
        raw = get_adzuna_jobs(
            what=keyword,
            where=location,
            page=page,
            results_per_page=per_page
        )
        jobs = normalize_adzuna_jobs(raw)
        if category:
            jobs = [job for job in jobs if category.lower() in job["category"].lower()]
    else:
        jobs = []

    def parse_date(job):
        return job.get("created", "")

    jobs.sort(key=parse_date, reverse=True)

    total = len(jobs)
    start = (page - 1) * per_page
    end = start + per_page
    jobs_paginated = jobs[start:end]
    total_pages = math.ceil(total / per_page)

    return render_template(
        "index.html",
        jobs=jobs_paginated,
        page=page,
        total_pages=total_pages,
        source=source
    )

