from flask import Blueprint, render_template

auth_page_bp = Blueprint('auth_page', __name__)

@auth_page_bp.route('/auth')
def auth():
    return render_template('auth.html')