from flask import Blueprint, render_template
from db import get_db_connection
from datetime import datetime, date

view_bp = Blueprint('view_tasks', __name__)

@view_bp.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute(
        '''
        SELECT id, task_name, task_description, due_date, status FROM tasks
        ORDER BY
            CASE
                WHEN due_date IS NULL OR due_date = '' THEN 1
                ELSE 0
            END,
            due_date ASC,
            id ASC
        '''
    ).fetchall()
    conn.close()
    today = date.today()
    overdue_tasks = []
    upcoming_tasks = []
    completed_tasks = []
    no_due_date_tasks = []
    for task in tasks:
        if not task['due_date']:
            no_due_date_tasks.append(task)
        else:
            task_due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            if task_due_date < today and task['status'] != 'Completed':
                overdue_tasks.append(task)
            elif task['status'] != 'Completed':
                upcoming_tasks.append(task)
            else:
                completed_tasks.append(task)
    return render_template('index.html', overdue_tasks = overdue_tasks, upcoming_tasks = upcoming_tasks, completed_tasks = completed_tasks, no_due_date_tasks = no_due_date_tasks)