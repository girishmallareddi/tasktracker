from flask import Flask
from db import init_db
from routes.tasks import register_task_routes
from routes.auth import register_auth_routes

DB_FILE = "tasks.db"

def create_app(database_path):
    app = Flask(__name__)
    app.config['DATABASE'] = database_path
    app.config['SECRET_KEY'] = 'dev-secret-key-123'  # Required for flash messages
    app.secret_key = "secret"
    with app.app_context():  
        print(f"Initializing database at: {app.config['DATABASE']}")
        init_db()
    register_task_routes(app)
    register_auth_routes(app)
    return app

app = create_app(DB_FILE)

if __name__ == "__main__":
    app.run(debug=True)
