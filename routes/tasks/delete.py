from flask import Blueprint, redirect, url_for
from db import get_db_connection

delete_bp = Blueprint('delete_task', __name__)

@delete_bp.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()

    conn.execute(
        'DELETE FROM tasks WHERE id = ?',
        (task_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('view_tasks.index'))
