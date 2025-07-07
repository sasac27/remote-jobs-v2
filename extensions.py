from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_user_route"

limiter = Limiter(get_remote_address, app=app)

@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    user = session.get(User, int(user_id))
    if user:
        session.expunge(user)  # ✅ Detach for safe use
    session.close()
    return user