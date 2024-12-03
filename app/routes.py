from flask import Blueprint, render_template

# Blueprint for the main routes
main = Blueprint('main', __name__)

# Render homepage template
@main.route('/')
def index():
    return render_template('index.html')

# Route for logging workouts
@main.route('/log_workout')
def log_workout():
    return "Log your workout here."

# Route for goal setting
@main.route('/goals')
def goals():
    return "Set your goals here."
