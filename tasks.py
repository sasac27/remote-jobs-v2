#tasks.py
from models import SessionLocal, Subscription
from jobs.remotive import get_data
from app import filter_jobs
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

def send_all_alerts():
    session = SessionLocal()
    subscriptions = session.query(Subscription).all()
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    for sub in subscriptions:
        jobs = get_data()
        filtered_jobs = filter_jobs(jobs, sub)
        if filtered_jobs:
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = sub.email
            msg['Subject'] = "Your Remote Job Alerts"
            body = f"Hi,\n\nHere are your latest remote job matches:\n\n"
            body += "\n".join([f"- {job['title']} ({job['url']})" for job in filtered_jobs])
            body += "\n\nThanks for using Remote Job Notifier!"
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email_user, email_pass)
                server.sendmail(email_user, sub.email, msg.as_string())
                print(f"✅ Sent {len(filtered_jobs)} jobs to {sub.email}")

    session.close()

if __name__ = "__main__":
    send_all_alerts()

