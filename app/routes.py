from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import SelectWorkoutTypeForm, RunForm, WeightliftingForm, GoalForm
from .models import Goal, Workout
from flask_login import login_required, current_user
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

main = Blueprint('main', __name__)

# Render homepage
@main.route('/')
def index():
    return render_template('index.html')

# Log workout
@main.route('/log_workout', methods=['GET', 'POST'])
@login_required
def log_workout():
    select_form = SelectWorkoutTypeForm()

    # Fetch workouts for the current user and sort by date (descending)
    user_workouts = Workout.select().where(Workout.user == current_user.id).order_by(Workout.date.desc())

    # Serialize workouts for display
    all_workouts = [
        {
            'id': workout.id,
            'type': workout.workout_type,
            'date': workout.date.strftime('%Y-%m-%d'),
            'details': (
                f"Run - Distance: {workout.distance} miles, Duration: {workout.duration} minutes"
                if workout.workout_type == "run"
                else f"Lift - {workout.exercise or 'Custom'}, Weight: {workout.weight} lbs, Sets: {workout.sets}, Reps: {workout.reps}"
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



# Delete workout
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

# Log run
@main.route('/log_workout/run', methods=['GET', 'POST'])
@login_required
def log_run():
    run_form = RunForm()
    if run_form.validate_on_submit():
        Workout.create(
            user=current_user.id,
            workout_type="run",
            date=run_form.date.data,
            distance=run_form.distance.data,
            duration=run_form.duration.data,
        )
        flash("Run logged successfully!", 'success')
        return redirect(url_for('main.log_workout'))
    return render_template('log_run.html', form=run_form)

# Log weightlifting
@main.route('/log_workout/weightlifting', methods=['GET', 'POST'])
@login_required
def log_weightlifting():
    lifting_form = WeightliftingForm()
    if lifting_form.validate_on_submit():
        # Check if a custom exercise name is provided
        exercise_name = lifting_form.exercise.data
        if exercise_name == 'custom':
            exercise_name = lifting_form.custom_exercise.data

        Workout.create(
            user=current_user.id,
            workout_type="weightlifting",
            date=lifting_form.date.data,
            exercise=exercise_name,  # Use the actual exercise name
            weight=lifting_form.weight.data,
            sets=lifting_form.sets.data,
            reps=lifting_form.reps.data,
            duration=lifting_form.duration.data,
        )
        flash("Weightlifting logged successfully!")
        return redirect(url_for('main.log_workout'))
    return render_template('log_weightlifting.html', form=lifting_form)


# Route for setting goals
@main.route('/set_goal', methods=['GET', 'POST'])
@login_required
def set_goal():
    form = GoalForm()
    if form.validate_on_submit():
        Goal.create(
            user=current_user.id,
            description=form.goal_description.data,
            target_date=form.target_date.data,
        )
        flash('Goal set successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('set_goal.html', form=form)

# Route to delete goals
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

# View progress
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
        progress = 0  # Default progress to 0%
        relevant_workouts = user_workouts.where(Workout.date <= goal.target_date)

        if "Run" in goal.description:
            # Extract target distance from the goal description
            match = re.search(r'\d+', goal.description)
            if match:
                target_distance = int(match.group())
                total_distance = sum(workout.distance or 0 for workout in relevant_workouts if workout.workout_type == "run")
                progress = min(int((total_distance / target_distance) * 100), 100)
                print(f"[DEBUG] Goal: {goal.description}, Target: {target_distance}, Total Distance: {total_distance}, Progress: {progress}%")

        elif "Lift" in goal.description:
            # Extract target weight from the goal description
            match = re.search(r'\d+', goal.description)
            if match:
                target_weight = int(match.group())
                total_weight = sum(workout.weight or 0 for workout in relevant_workouts if workout.workout_type == "weightlifting")
                progress = min(int((total_weight / target_weight) * 100), 100)
                print(f"[DEBUG] Goal: {goal.description}, Target: {target_weight}, Total Weight: {total_weight}, Progress: {progress}%")

        elif "workout" in goal.description.lower():
            # Handle workout frequency goals
            match = re.search(r'\d+', goal.description)
            if match:
                target_workouts = int(match.group())
                monthly_workouts = sum(1 for workout in relevant_workouts if workout.date.month == today.month and workout.date.year == today.year)
                progress = min(int((monthly_workouts / target_workouts) * 100), 100)
                print(f"[DEBUG] Goal: {goal.description}, Target Workouts: {target_workouts}, Monthly Workouts: {monthly_workouts}, Progress: {progress}%")

        # Append the computed progress for each goal
        progress_data.append({
            'goal_id': goal.id,
            'goal': goal.description,
            'progress': progress,
            'target_date': goal.target_date,
        })

    # Render the progress template with the calculated data
    return render_template('progress.html', progress_data=progress_data)


# Weekly workout progress chart
@main.route('/progress/weekly_chart')
@login_required
def weekly_chart():
    week_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    workout_durations = {day: 0 for day in week_days}
    user_workouts = Workout.select().where(Workout.user == current_user.id)

    for workout in user_workouts:
        day_name = workout.date.strftime('%A')
        if day_name in workout_durations:
            if workout.workout_type == 'run' or workout.workout_type == 'weightlifting':
                workout_durations[day_name] += workout.duration or 0 


    fig, ax = plt.subplots(figsize=(15, 9))
    bars = ax.bar(workout_durations.keys(), workout_durations.values(), color='blue')

    ax.set_ylabel('Duration (minutes)', fontsize=12)
    ax.set_xlabel('Day', fontsize=12)
    ax.set_ylim(0, 240)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    chart_url = base64.b64encode(buffer.getvalue()).decode('utf8')
    buffer.close()

    return render_template('weekly_workout_chart.html', chart_url=chart_url)

