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
    if select_form.validate_on_submit():
        if select_form.workout_type.data == 'run':
            return redirect(url_for('main.log_run'))
        elif select_form.workout_type.data == 'weightlifting':
            return redirect(url_for('main.log_weightlifting'))
    return render_template('select_workout_type.html', form=select_form)

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
@login_required
def progress():
    user_goals = Goal.select().where(Goal.user == current_user.id)
    user_workouts = Workout.select().where(Workout.user == current_user.id)

    progress_data = []
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    for goal in user_goals:
        if "Run" in goal.description:
            total_distance = sum(workout.duration for workout in user_workouts if workout.workout_type == "run")
            progress = min(int((total_distance / goal.target_value) * 100), 100)

        elif "Lift" in goal.description:
            total_weight = sum(workout.weight for workout in user_workouts if workout.workout_type == "weightlifting")
            progress = min(int((total_weight / goal.target_value) * 100), 100)

        elif "workout" in goal.description.lower():
            match = re.search(r'\d+', goal.description)
            if match:
                target_workouts = int(match.group())
                monthly_workouts = sum(1 for workout in user_workouts if workout.date.month == current_month and workout.date.year == current_year)
                progress = min(int((monthly_workouts / target_workouts) * 100), 100)
            else:
                progress = 0

        else:
            progress = 0

        progress_data.append({
            'goal': goal.description,
            'progress': progress,
        })

    return render_template('progress.html', progress_data=progress_data)


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
    fig, ax = plt.subplots()
    ax.bar(workout_durations.keys(), workout_durations.values(), color='blue')
    ax.set_title('Weekly Workout Progress')
    ax.set_ylabel('Duration (minutes)')
    ax.set_xlabel('Day')

    # Save the chart to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_url = base64.b64encode(buffer.getvalue()).decode('utf8')
    buffer.close()

    return render_template('weekly_workout_chart.html', chart_url=chart_url)