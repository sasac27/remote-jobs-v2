from backend.routes.api_auth import api_auth_bp
from backend.routes.subscriptions import sub_bp
from backend.routes.jobs import jobs_bp 
from backend.routes.analytics import analytics_bp
from backend.routes.dashboard import dashboard_bp

def register_routes(app):
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(sub_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(dashboard_bp)
