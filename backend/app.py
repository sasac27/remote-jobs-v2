# app.py

from flask import Flask, jsonify, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apscheduler import APScheduler
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

from backend.models import Base, engine, SessionLocal, User
from backend.config import Config
from backend.routes import register_routes
from backend.routes.api_auth import api_auth_bp
from backend.routes.subscriptions import sub_bp
from backend.routes.jobs import jobs_bp
from backend.routes.dashboard import dashboard_bp
from backend.api.jobs.tasks import fetch_and_store_jobs

# Load environment variables
load_dotenv()

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Flask extensions
csrf = CSRFProtect()
limiter = Limiter(get_remote_address)


def create_app():
    Base.metadata.create_all(bind=engine)

    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    limiter.init_app(app)

    #Load CORS origin
    ALLOWED_ORIGIN = os.getenv("CORS_ORIGIN", "https://remote-jobs-v2-1.onrender.com")

    # Enable CORS for frontend requests (Angular)
    CORS(app, supports_credentials=True, origins=[ALLOWED_ORIGIN])


    # Exempt CSRF for API routes
    csrf.exempt(api_auth_bp)
    csrf.exempt(sub_bp)
    csrf.exempt(jobs_bp)
    csrf.exempt(dashboard_bp)

    @app.route("/")
    def index():
        return redirect(url_for("api.api_get_jobs"))
    
    @app.before_request
    def log_request_headers():
        from flask import request
        print("\n=== Incoming Request ===")
        print("Method:", request.method)
        print("Path:", request.path)
        for header, value in request.headers.items():
            print(f"{header}: {value}")

    # Register all route blueprints
    register_routes(app)

    return app

# Initialize app
app = create_app()

# JWT config
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default-dev-secret")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]  # 👈 explicitly allow header-based tokens
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
jwt = JWTManager(app)


# Scheduler setup
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_job(id='Fetch Job Data', func=fetch_and_store_jobs, trigger='interval', hours=6)
scheduler.start()

# Context processors
@app.context_processor
def inject_global():
    return {"current_year": datetime.now().year}

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    fetch_and_store_jobs()
    app.run(debug=True)
