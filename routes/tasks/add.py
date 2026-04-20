from flask import Blueprint, request, session, redirect, url_for, flash
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
    
    if name and len(name) > 50:
        flash(f"Error: Task name must be 50 characters or less. Current length: {len(name)} characters.", 'error')
        return redirect(url_for('view_tasks.index'))
    
    if desc and len(desc) > 500:
        flash(f"Error: Description must be 500 characters or less. Current length: {len(desc)} characters.", 'error')
        return redirect(url_for('view_tasks.index'))

    if name and desc:
        conn = get_db_connection()
        conn.execute(
            '''
            INSERT INTO tasks (user_id,task_name, task_description, due_date, status)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (session['user_id'],name, desc, due_date, status)
        )
        conn.commit()
        conn.close()
        flash(f"Task '{name}' added successfully!", 'success')

    return redirect(url_for('view_tasks.index'))
