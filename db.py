import sqlite3
from flask import current_app

DB_FILE = "tasks.db"


def get_db_connection():
    db = current_app.config.get('DATABASE', DB_FILE)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_name TEXT NOT NULL,
            task_description TEXT NOT NULL,
            due_date TEXT,
            status TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
    conn.commit()
    conn.close()


def is_task_name_duplicate(task_name, exclude_id=None):
    conn = get_db_connection()
    
    if exclude_id is not None:
        # For edit operations: check duplicates excluding the current task
        result = conn.execute(
            'SELECT task_name FROM tasks WHERE id != ?',
            (exclude_id,)
        ).fetchall()
    else:
        # For add operations: check all tasks
        result = conn.execute('SELECT task_name FROM tasks').fetchall()
    
    conn.close()
    
    # Case-insensitive comparison
    existing_names = [task['task_name'].lower() for task in result]
    return task_name.lower() in existing_names
