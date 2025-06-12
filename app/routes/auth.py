from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # login logic goes here (e.g., check username and password)
        return redirect(url_for('index.html'))
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # signup logic goes here (e.g., create a new user)
        return redirect(url_for('auth_bp.login'))
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    # logout logic goes here (e.g., clear session)
    return redirect(url_for('index.html'))