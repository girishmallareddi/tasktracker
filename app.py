from flask import Flask
from db import init_db
from routes.tasks import register_task_routes

DB_FILE = "tasks.db"

def create_app(database_path):
    app = Flask(__name__)
    app.config['DATABASE'] = database_path
    app.config['SECRET_KEY'] = 'dev-secret-key-123'  # Required for flash messages
    with app.app_context():  
        init_db()
    register_task_routes(app)
    return app

app = create_app(DB_FILE)

if __name__ == "__main__":
    app.run(debug=True)
