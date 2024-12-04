from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        try:
            User.create(username=username, email=email, password=hashed_password)
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('An account with that username or email already exists.', 'danger')

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Attempting login with email: {email}")  # Debugging

        user = User.get_or_none(User.email == email)
        if user:
            print("User found in database.")  # Debugging
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.index'))
            else:
                print("Password does not match.")  # Debugging
        else:
            print("No user found with that email.")  # Debugging

        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
