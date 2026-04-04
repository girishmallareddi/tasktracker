from flask import Blueprint, request, redirect, url_for, flash
from db import get_db_connection, is_task_name_duplicate

edit_bp = Blueprint('edit_task', __name__)

@edit_bp.route('/edittask/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    name = request.form.get('task_name')
    desc = request.form.get('task_description')
    due_date = request.form.get('due_date')
    status = request.form.get('status')

    # Check if task name already exists (excluding current task)
    if name and is_task_name_duplicate(name, exclude_id=task_id):
        flash(f"Error: Task name '{name}' already exists. Please choose a different name.", 'error')
        return redirect(url_for('view_tasks.index'))

    conn = get_db_connection()

    task = conn.execute(
        'SELECT * FROM tasks WHERE id = ?',
        (task_id,)
    ).fetchone()

    if task:
        conn.execute("""
            UPDATE tasks
            SET task_name = COALESCE(?, task_name),
                task_description = COALESCE(?, task_description),
                due_date = COALESCE(?, due_date),
                status = COALESCE(?, status)
            WHERE id = ?
        """, (name, desc, due_date, status, task_id))
        conn.commit()
        flash(f"Task '{name}' updated successfully!", 'success')

    conn.close()
    return redirect(url_for('view_tasks.index'))
