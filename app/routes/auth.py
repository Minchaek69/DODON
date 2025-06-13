from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        next_page = request.form.get('next') or url_for('main.index')  

        if not email or not password or password != confirm:
            flash('Please fill all fields correctly.', 'error')
            return redirect(url_for('auth_bp.signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth_bp.signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, is_admin=False)  
        db.session.add(new_user)
        db.session.commit()

        session['user_email'] = new_user.email
        session['is_admin'] = new_user.is_admin

        flash('Signup successful! Logged in.', 'success')
    next_page = request.form.get('next') or url_for('main.index')
    return redirect(next_page)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        next_page = request.form.get('next') or url_for('main.index')  

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_email'] = user.email
            session['is_admin'] = user.is_admin

            flash('Login successful!', 'success')
            
            if user.is_admin:
                flash('Welcome, Admin!', 'info')
                return redirect(url_for('admin_bp.admin_products'))
            else:
                return redirect(next_page)
        else:
            flash('Invalid email or password.', 'error')
    next_page = request.form.get('next') or url_for('main.index')
    return redirect(next_page)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    next_page = request.args.get('next') or url_for('main.index')  
    return redirect(next_page)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_email') or not session.get('is_admin'):
            flash('Admin access required.')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function


