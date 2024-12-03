from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import WorkoutForm, GoalForm
from .models import Workout, Goal

# Blueprint for the main routes
main = Blueprint('main', __name__)

# Render homepage template
@main.route('/')
def index():
    return render_template('index.html')

# Route for logging workouts
@main.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        # Save the workout to the database
        Workout.create(
            user=1,  # Replace with the actual user ID
            workout_type=form.workout_type.data,
            date=form.date.data,
            duration=form.duration.data,
            intensity=form.intensity.data,
            notes=form.notes.data
        )
        flash('Workout logged successfully!')
        return redirect(url_for('main.index'))
    return render_template('log_workout.html', form=form)

# Route for goal setting
@main.route('/set_goal', methods=['GET', 'POST'])
def set_goal():
    form = GoalForm()
    if form.validate_on_submit():
        # Save the goal to the database
        Goal.create(
            user=1,  # Replace with the actual user ID
            description=form.goal_description.data,
            target_date=form.target_date.data,
            target_value=form.target_value.data
        )
        flash('Goal set successfully!')
        return redirect(url_for('main.index'))
    return render_template('set_goal.html', form=form)

# Route for viewing progress
@main.route('/progress')
def progress():
    return render_template('progress.html')