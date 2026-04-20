from .login import login_bp
from .register import register_bp
from .logout import logout_bp
from .auth_page import auth_page_bp

def register_auth_routes(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(auth_page_bp)