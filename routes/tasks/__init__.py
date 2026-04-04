from .view import view_bp
from .add import add_bp
from .edit import edit_bp
from .delete import delete_bp

def register_task_routes(app):
    app.register_blueprint(view_bp)
    app.register_blueprint(add_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(delete_bp)