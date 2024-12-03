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
    try:
        # Fetch the user's goals and workouts
        user_goals = Goal.select().where(Goal.user == 1)  # Replace with actual user ID
        user_workouts = Workout.select().where(Workout.user == 1)
        
        if not user_goals.exists() or not user_workouts.exists():
            # If no goals or workouts, raise an exception
            raise ValueError("No progress data available. Please add goals or log workouts first.")
        
        # Process data to calculate progress
        progress_data = []
        for goal in user_goals:
            # Example: count workouts towards a goal
            workouts_completed = user_workouts.count()
            percentage = min(int((workouts_completed / goal.target_value) * 100), 100)
            progress_data.append({
                'goal': goal.description,
                'progress': percentage
            })
        
        return render_template('progress.html', progress_data=progress_data)

    except ValueError as e:
        # Display the error message in the template
        return render_template('progress.html', error_message=str(e))