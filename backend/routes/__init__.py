from routes.api_auth import api_auth_bp
from routes.subscriptions import sub_bp
from routes.jobs import jobs_bp 
from routes.analytics import analytics_bp
from routes.dashboard import dashboard_bp

def register_routes(app):
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(sub_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(dashboard_bp)
