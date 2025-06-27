# routes/analytics.py
from flask import Blueprint, jsonify
from sqlalchemy import func, desc, cast, Date
from models import SessionLocal, JobPost, Subscription

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/api/analytics/job-counts", methods=["GET"])
def job_counts():
    with SessionLocal() as db:
        counts = db.query(JobPost.category, func.count(JobPost.id)) \
            .group_by(JobPost.category) \
            .order_by(desc(func.count(JobPost.id))) \
            .all()
        return jsonify([{"category": c or "Uncategorized", "count": n} for c, n in counts])


@analytics_bp.route("/api/analytics/location-trends", methods=["GET"])
def location_trends():
    with SessionLocal() as db:
        counts = db.query(JobPost.location, func.count(JobPost.id)) \
            .group_by(JobPost.location) \
            .order_by(desc(func.count(JobPost.id))) \
            .all()
        return jsonify([{"location": loc or "Unknown", "count": n} for loc, n in counts])


@analytics_bp.route("/api/analytics/salary-data", methods=["GET"])
def salary_data():
    with SessionLocal() as db:
        salaries = db.query(JobPost.salary).filter(JobPost.salary.isnot(None)).limit(200).all()
        return jsonify([s[0] for s in salaries if s[0]])


@analytics_bp.route("/api/analytics/posting-timeline", methods=["GET"])
def posting_timeline():
    with SessionLocal() as db:
        timeline = db.query(
            cast(JobPost.created_at, Date).label('date'),
            func.count(JobPost.id)
        ).group_by('date').order_by('date').all()
        return jsonify([{"date": str(d), "count": c} for d, c in timeline])


@analytics_bp.route("/api/analytics/subscriptions", methods=["GET"])
def subscription_counts():
    with SessionLocal() as db:
        counts = db.query(Subscription.category, func.count(Subscription.id)) \
            .group_by(Subscription.category) \
            .order_by(desc(func.count(Subscription.id))) \
            .all()
        return jsonify([{"category": c or "Unspecified", "count": n} for c, n in counts])
