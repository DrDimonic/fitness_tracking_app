# Fitness Tracker

## Overview
This is a Fitness Tracker application which allows users to log workouts, set fitness goals, and track their progress over time. Built using Python, Flask, and Peewee ORM, it includes user authentication, visual data representations, and dynamic progress tracking to enhance the user experience.

## Setup
1. Clone the repository 
    - git clone https://github.com/DrDimonic/fitness_tracking_app
    - cd fitness_tracking_app
2. Create a virtual environment
    - venv
3. Install dependencies
    - pip install -r requirements.txt
4. Initialize the Database
    - python initialize_db.py
5. Run the application
    - python main.py
6. Open application in browser
    - Navigate to http://127.0.0.1:5000

## Prerequisites
- Python 3.9
- Venv
- Flask
- Peewee ORM
- Matplotlib

## Dependencies
- Flask
- Flask-login
- Flask-bcrypt
- Flask-wtf
- Peewee
- Matplotlib
- WTForms

## Main Python Files
- main.py: The entry point of the application.
- initialize_db.py: Initializes the database.
- app/__init__.py: Initializes Flask, Peewee ORM, and application configurations.
- app/models.py: Defines database models (e.g., users, workouts, goals).
- app/routes.py: Contains the main routes for the application (e.g., logging workouts, progress tracking).
- app/authenticate.py: Handles user registration, login, and logout.

## Main HTML Files (Templates)
- index.html: The homepage.
- login.html: Login screen.
- register.html: User registration form.
- progress.html: Displays user progress and goals.
- weekly_workout_chart.html: Visual representation of weekly workout durations.
- select_workout_type.html: Page to select workout types and view/delete past workouts.
- set_goal.html: Page to set fitness goals.
- log_run.html & log_weightlifting.html: Forms for logging workouts.

## Features
- User authentication
    - Secure login and registration.
- Workout logging
    - Log running and weightlifting workouts with customizable inputs.
- Goal setting & tracking
    - Set fitness goals such as running a specific distance or lifting a target weight.
    - View goal progress with dynamic progress bars.
- Visual Data Representation
    - Weekly workout chart showing total time spent working out each day.