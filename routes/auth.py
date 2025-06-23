# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import SessionLocal, User
import re

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_user_route():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.", "danger")
            return render_template("login.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return render_template("login.html")

        session = SessionLocal()
        try:
            user = session.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                session.expunge(user)
                login_user(user)
                flash("Login successful.", "success")
                return redirect(request.args.get("next") or url_for("paginated_jobs_route"))
            else:
                flash("Wrong username or password.", "danger")
        finally:
            session.close()

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout_user_route():
    logout_user()
    flash("Logout successful.")
    return redirect("/")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.", "danger")
            return redirect("/register")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect("/register")

        with SessionLocal() as session:
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                flash("An account with this email already exists.", "warning")
                return redirect("/register")

            user = User(email=email, password_hash=generate_password_hash(password))
            session.add(user)
            session.commit()

        flash("✅ Account created! Please log in.", "info")
        return redirect("/login")

    return render_template("register.html")
