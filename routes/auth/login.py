from flask import Blueprint, request, redirect, url_for, session, flash
from db import get_db_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']  
        flash("Login successful!", "success")
        return redirect(url_for('view_tasks.index'))
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for('view_tasks.index'))