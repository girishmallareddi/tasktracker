from flask import Blueprint, request, redirect, url_for, flash
from db import get_db_connection

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        flash("Registration successful! Please login.", "success")
    except:
        flash("User already exists", "error")

    conn.close()
    return redirect(url_for('view_tasks.index'))