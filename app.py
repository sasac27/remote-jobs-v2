# app.py
from flask import Flask
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apscheduler import APScheduler
from flask_wtf import CSRFProtect
from models import Base, engine
from config import Config
from routes import register_routes  # 👈 this imports all your modular routes
from models import SessionLocal, User
from datetime import datetime
from jobs.tasks import fetch_and_store_jobs

csrf = CSRFProtect()
login_manager = LoginManager()



@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    user = session.get(User, int(user_id))
    if user:
        session.expunge(user)
    session.close()
    return user

limiter = Limiter(get_remote_address)

def create_app():
    Base.metadata.create_all(bind=engine)

    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    login_manager.login_view = "auth.login_user_route"
    register_routes(app)  # 👈 mount routes from blueprint modules

    return app

app = create_app()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='Fetch Job Data', func=fetch_and_store_jobs, trigger='interval', hours=6)
@app.context_processor
def inject_global():
    return {"current_year": datetime.now().year}


if __name__ == "__main__":
    app.run(debug=True)
