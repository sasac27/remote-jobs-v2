# routes/__init__.py
from .auth import auth_bp
from .jobs import jobs_bp
from .subscriptions import sub_bp
from .dashboard import dashboard_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(sub_bp)
    app.register_blueprint(dashboard_bp)
