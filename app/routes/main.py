from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/profile')
def profile():
    if not session.get('user_email'):
        return redirect(url_for('auth_bp.login')) 
    return render_template('profile.html', user_email=session['user_email'])