# routes/subscriptions.py

from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from backend.models import SessionLocal, Subscription, User
from backend.api.jobs.remotive import get_remotive_jobs
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_jwt_extended import jwt_required, get_jwt_identity

sub_bp = Blueprint("subscriptions", __name__)


@sub_bp.route("/api/subscriptions", methods=["POST"])
@jwt_required()
def api_create_subscription():
    data = request.get_json()
    email = get_jwt_identity()

    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404

        sub = Subscription(
            user_id=user.id,
            email=email,
            category=data.get("category"),
            location=data.get("location"),
            keyword=data.get("keyword")
        )
        session.add(sub)
        session.commit()

    return jsonify({"msg": "Subscription saved!"}), 201


@sub_bp.route("/api/subscriptions", methods=["GET"])
@jwt_required()
def api_get_subscriptions():
    email = get_jwt_identity()

    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404

        subs = [
            {
                "id": s.id,
                "email": s.email,
                "category": s.category,
                "location": s.location,
                "keyword": s.keyword
            }
            for s in user.subscriptions
        ]
    return jsonify(subs), 200


@sub_bp.route("/subscribe", methods=["GET", "POST"])
@login_required
def subscribe_to_email():
    if request.method == "POST":
        sub = Subscription(
            user_id=current_user.id,
            email=current_user.email,
            category=request.form.get("category"),
            location=request.form.get("location"),
            keyword=request.form.get("keyword")
        )
        with SessionLocal() as session:
            session.add(sub)
            session.commit()
        return "Subscription saved!"
    return render_template("subscribe.html")

@sub_bp.route("/send-alert")
@login_required
def send_alert():
    with SessionLocal() as session:
        subscriptions = session.query(Subscription).filter_by(user_id=current_user.id).all()
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        jobs = get_remotive_jobs()
        sent_count = 0
        for sub in subscriptions:
            filtered_jobs = filter_jobs(jobs, sub)
            if filtered_jobs:
                send_email_alert(sub.email, filtered_jobs, email_user, email_pass)
                sent_count += 1
        flash(f"✅ Sent alerts to {sent_count} subscriptions." if sent_count else "No matching jobs to send", "info")
    return redirect(url_for("jobs.paginated_jobs_route"))

def send_email_alert(to_email, jobs, email_user, email_pass):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = "Your Remote Job Alerts"
    body = "Hi,\n\nHere are your latest remote job matches:\n\n"
    body += "\n".join([f"- {job['title']} ({job['url']})" for job in jobs])
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, to_email, msg.as_string())

def filter_jobs(jobs, sub):
    return [job for job in jobs if
            (not sub.category or sub.category.lower() in job["category"].lower()) and
            (not sub.location or sub.location.lower() in job["location"].lower()) and
            (not sub.keyword or sub.keyword.lower() in job["title"].lower() or sub.keyword.lower() in job["description"].lower())]
