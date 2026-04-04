from flask import Blueprint, request, redirect, url_for, flash
from db import get_db_connection, is_task_name_duplicate

add_bp = Blueprint('add_task', __name__)

@add_bp.route('/addtask', methods=['POST'])
def add_task():
    name = request.form.get('task_name')
    desc = request.form.get('task_description')
    due_date = request.form.get('due_date')
    status = request.form.get('status')

    # Check if task name already exists
    if name and is_task_name_duplicate(name):
        flash(f"Error: Task name '{name}' already exists. Please choose a different name.", 'error')
        return redirect(url_for('view_tasks.index'))

    if name and desc:
        conn = get_db_connection()
        conn.execute(
            '''
            INSERT INTO tasks (task_name, task_description, due_date, status)
            VALUES (?, ?, ?, ?)
            ''',
            (name, desc, due_date, status)
        )
        conn.commit()
        conn.close()
        flash(f"Task '{name}' added successfully!", 'success')

    return redirect(url_for('view_tasks.index'))
