from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import SelectWorkoutTypeForm, RunForm, WeightliftingForm, GoalForm
from .models import Goal, Workout, User
from flask_login import login_required, current_user
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
import datetime

matplotlib.use('Agg')

# Blueprint for the main routes
main = Blueprint('main', __name__)

# Render homepage template
@main.route('/')
def index():
    return render_template('index.html')

# Route for logging workouts
@main.route('/log_workout', methods=['GET', 'POST'])
@login_required
def log_workout():
    select_form = SelectWorkoutTypeForm()
    user_workouts = Workout.select().where(Workout.user == current_user.id)

    # Serialize workouts for display
    all_workouts = [
        {
            'id': workout.id,
            'type': workout.workout_type,
            'date': workout.date.strftime('%Y-%m-%d'),
            'details': (
                f"Distance: {workout.duration} miles, Time: {workout.duration} minutes"
                if workout.workout_type == "run"
                else f"Exercise: {workout.exercise}, Weight: {workout.weight} lbs, Sets: {workout.sets}, Reps: {workout.reps}"
            )
        }
        for workout in user_workouts
    ]

    if select_form.validate_on_submit():
        if select_form.workout_type.data == 'run':
            return redirect(url_for('main.log_run'))
        elif select_form.workout_type.data == 'weightlifting':
            return redirect(url_for('main.log_weightlifting'))
    
    return render_template(
        'select_workout_type.html',
        form=select_form,
        all_workouts=all_workouts
    )

# Route for deleting workouts
@main.route('/delete_workout/<int:workout_id>', methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.get_or_none(Workout.id == workout_id, Workout.user == current_user.id)
    if workout:
        workout.delete_instance()
        flash('Workout deleted successfully.', 'success')
    else:
        flash('Workout not found or unauthorized.', 'danger')
    return redirect(url_for('main.log_workout'))


# Route for logging a run
@main.route('/log_workout/run', methods=['GET', 'POST'])
@login_required
def log_run():
    run_form = RunForm()
    if run_form.validate_on_submit():
        distance = run_form.distance.data
        time = run_form.time.data

        # Save the workout with the current user's ID
        Workout.create(
            user=current_user.id,
            workout_type="run",
            date=run_form.date.data,
            duration=time,
            intensity=None,
            exercise=None,
            weight=None,
            sets=None,
            reps=None
        )

        flash("Run logged successfully!")
        return redirect(url_for('main.log_workout'))
    return render_template('log_run.html', form=run_form)


# Route for logging a lift
@main.route('/log_workout/weightlifting', methods=['GET', 'POST'])
@login_required
def log_weightlifting():
    lifting_form = WeightliftingForm()
    if lifting_form.validate_on_submit():
        Workout.create(
            user=current_user.id,
            workout_type="weightlifting",
            date=lifting_form.date.data,
            exercise=lifting_form.exercise.data,
            weight=lifting_form.weight.data,
            sets=lifting_form.sets.data,
            reps=lifting_form.reps.data
        )

        flash("Weightlifting logged successfully!")
        return redirect(url_for('main.log_workout'))
    return render_template('log_weightlifting.html', form=lifting_form)

# Route for goal setting
@main.route('/set_goal', methods=['GET', 'POST'])
@login_required
def set_goal():
    form = GoalForm()
    if form.validate_on_submit():
        # Save the goal to the database
        Goal.create(
            user=current_user.id,
            description=form.goal_description.data,
            target_date=form.target_date.data,
        )
        flash('Goal set successfully!')
        return redirect(url_for('main.index'))
    return render_template('set_goal.html', form=form)

# Route for viewing progress
@main.route('/progress')
@login_required
def progress():
    import re
    from datetime import datetime

    # Fetch user's goals and workouts
    user_goals = Goal.select().where(Goal.user == current_user.id)
    user_workouts = Workout.select().where(Workout.user == current_user.id)

    progress_data = []
    today = datetime.now()

    for goal in user_goals:
        # Filter workouts up to the target date
        relevant_workouts = user_workouts.where(Workout.date <= goal.target_date)

        if "Run" in goal.description:
            # Extract target distance from the goal description
            match = re.search(r'\d+', goal.description)
            if match:
                target_distance = int(match.group())
                total_distance = sum(workout.duration for workout in relevant_workouts if workout.workout_type == "run")
                progress = min(int((total_distance / target_distance) * 100), 100)
            else:
                progress = 0  # Default if no target is found

        elif "Lift" in goal.description:
            # Extract target weight from the goal description
            match = re.search(r'\d+', goal.description)
            if match:
                target_weight = int(match.group())
                total_weight = sum(workout.weight for workout in relevant_workouts if workout.workout_type == "weightlifting")
                progress = min(int((total_weight / target_weight) * 100), 100)
            else:
                progress = 0  # Default if no target is found

        elif "workout" in goal.description.lower():
            # Handle workout frequency goals
            match = re.search(r'\d+', goal.description)
            if match:
                target_workouts = int(match.group())
                monthly_workouts = sum(1 for workout in relevant_workouts if workout.date.month == today.month and workout.date.year == today.year)
                progress = min(int((monthly_workouts / target_workouts) * 100), 100)
            else:
                progress = 0  # Default if no target is found

        else:
            progress = 0  # Default for unrecognized goal types

        # Append progress data
        progress_data.append({
            'goal_id': goal.id,
            'goal': goal.description,
            'progress': progress,
            'target_date': goal.target_date,
        })

    return render_template('progress.html', progress_data=progress_data)

# Route for removing goals
@main.route('/delete_goal/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.get_or_none(Goal.id == goal_id, Goal.user == current_user.id)
    if goal:
        goal.delete_instance()
        flash('Goal deleted successfully.', 'success')
    else:
        flash('Goal not found or unauthorized.', 'danger')
    return redirect(url_for('main.progress'))


# Route for weekly workout progress chart
@main.route('/progress/weekly_chart')
@login_required
def weekly_chart():
    # Initialize the week (Sunday to Saturday)
    week_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    workout_durations = {day: 0 for day in week_days}

    # Fetch user's workouts
    user_workouts = Workout.select().where(Workout.user == current_user.id)

    for workout in user_workouts:
        day_name = workout.date.strftime('%A')  # Get the day name (e.g., "Monday")
        if day_name in workout_durations:
            workout_durations[day_name] += workout.duration or 0

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(25, 10))  # Set chart size (10 inches by 6 inches)
    bars = ax.bar(workout_durations.keys(), workout_durations.values(), color='blue')  # Green bars

    # Customize the chart
    ax.set_ylabel('Duration (minutes)', fontsize=18)
    ax.set_xlabel('Day', fontsize=18)
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylim(0, 240)

    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', fontsize=12)

    # Save the chart to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')  # Ensure tight layout
    buffer.seek(0)
    chart_url = base64.b64encode(buffer.getvalue()).decode('utf8')
    buffer.close()

    return render_template('weekly_workout_chart.html', chart_url=chart_url)