from flask import Blueprint, render_template, redirect, url_for, request, flash
from .forms import WorkoutForm, GoalForm
from .models import db, Workout, User

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
        # Save workout data to the database
        Workout.create(
            user=1,  # Placeholder; replace with logged-in user's ID
            workout_type=form.workout_type.data,
            date=form.date.data,
            duration=form.duration.data,
            intensity=form.intensity.data,
            notes=form.notes.data
        )
        flash("Workout logged successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template('log_workout.html', form=form)

# Route for goal setting
@main.route('/set_goal', methods=['GET', 'POST'])
def set_goal():
    form = GoalForm()
    if form.validate_on_submit():
        # Save goal data to the database (add Goal model if needed)
        flash("Goal set successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template('set_goal.html', form=form)

# Route for viewing progress
@main.route('/progress')
def progress():
    # Example progress calculation
    total_workouts = Workout.select().count()
    # Replace with actual goal-tracking logic
    return render_template('progress.html', total_workouts=total_workouts)