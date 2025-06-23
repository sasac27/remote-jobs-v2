from flask import Blueprint, render_template
from flask_login import login_required
from utils.job_data import get_all_jobs
from collections import Counter
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    jobs = get_all_jobs()
    total_jobs = len(jobs)

    categories = [job["category"] for job in jobs if "category" in job]
    locations = [job["location"] for job in jobs if "location" in job]

    top_categories = Counter(categories).most_common(5)
    top_locations = Counter(locations).most_common(5)

    salaries = [job["salary_num"] for job in jobs if job.get("salary_num") and isinstance(job["salary_num"], (int, float))]

    buckets = {
        "0-50k": 0,
        "50k-100k": 0,
        "100k-150k": 0,
        "150k-200k": 0,
        "200k+": 0
    }

    for s in salaries:
        if s < 50000:
            buckets["0-50k"] += 1
        elif s < 100000:
            buckets["50k-100k"] += 1
        elif s < 150000:
            buckets["100k-150k"] += 1
        elif s < 200000:
            buckets["150k-200k"] += 1
        else:
            buckets["200k+"] += 1

    missing_salaries = len(jobs) - len(salaries)


    #Group jobs by posting date (round to day)
    date_counts = Counter()
    for job in jobs:
        if "created" in job:
            try:
                dt = datetime.fromisoformat(job["created"]).date()
                date_counts[dt] += 1
            except Exception:
                continue
    #Sort chronologically
    trend_data = sorted(date_counts.items())
    trend_labels = [d.strftime("%Y-%m-%d") for d, _ in trend_data]
    trend_values = [count for _, count in trend_data]
    
    return render_template("dashboard.html", total_jobs=total_jobs,
                           top_categories=top_categories,
                           top_locations=top_locations,
                           salary_distribution=buckets,
                           missing_salaries=missing_salaries,
                           salaries=salaries,
                           trend_labels=trend_labels,
                           trend_values=trend_values)