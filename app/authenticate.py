from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required
from .models import User
from . import bcrypt

# Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Route to handle user registration
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password for secure storage
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        try:
            User.create(username=username, email=email, password=hashed_password)
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('An account with that username or email already exists.', 'danger')

    return render_template('register.html')

# Route to handle user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_or_none(User.email == email)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    session.clear() 
    return redirect(url_for('auth.login'))

