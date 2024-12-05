from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import SelectWorkoutTypeForm, RunForm, WeightliftingForm, GoalForm
from .models import Goal, Workout, User
from flask_login import login_required, current_user


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
def log_run():
    run_form = RunForm()
    if run_form.validate_on_submit():
        # Calculate calories burned and average speed
        distance = run_form.distance.data
        time = run_form.time.data
        avg_speed = distance / (time / 60)  # Average speed in mph
        calories_burned = distance * 100  # Approximate calorie burn

        # Save to database (example only)
        flash(f"Run logged! Calories burned: {calories_burned} | Avg speed: {avg_speed:.2f} mph")
        return redirect(url_for('main.log_workout'))
    return render_template('log_run.html', form=run_form)

# Route for logging a lift
@main.route('/log_workout/weightlifting', methods=['GET', 'POST'])
def log_weightlifting():
    lifting_form = WeightliftingForm()
    if lifting_form.validate_on_submit():
        # Get user input
        exercise = lifting_form.exercise.data
        if exercise == 'custom':
            exercise = lifting_form.custom_exercise.data

        weight = lifting_form.weight.data
        sets = lifting_form.sets.data
        reps = lifting_form.reps.data  # Capture repetitions
        difficulty = lifting_form.difficulty.data

        # Calculate calories burned (example logic)
        difficulty_multiplier = {'easy': 3, 'moderate': 5, 'hard': 8}
        calories_burned = sets * reps * weight * difficulty_multiplier[difficulty]

        # Save to database
        Workout.create(
            user=current_user.id,
            workout_type="weightlifting",
            date=lifting_form.date.data,
            exercise=exercise,
            weight=weight,
            sets=sets,
            reps=reps,
            intensity=None
        )

        flash(f"Weightlifting logged! Calories burned: {calories_burned}")
        return redirect(url_for('main.log_workout'))
    return render_template('log_weightlifting.html', form=lifting_form)

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
@login_required
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

# Route for creating pie charts
@main.route('/progress/pie_chart/<int:goal_id>')
def pie_chart(goal_id):
    goal = Goal.get_or_none(Goal.id == goal_id)
    if not goal:
        return "Goal not found", 404

    workouts_completed = Workout.select().where(Workout.user == goal.user).count()
    remaining = max(goal.target_value - workouts_completed, 0)

    labels = ['Completed', 'Remaining']
    sizes = [workouts_completed, remaining]
    colors = ['#4CAF50', '#FF9999']  # Green and red

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_url = base64.b64encode(buffer.getvalue()).decode('utf8')
    buffer.close()

    return render_template('pie_chart.html', plot_url=plot_url, goal=goal)

# Route for creating line charts
@main.route('/progress/line_chart/<int:goal_id>')
def line_chart(goal_id):
    goal = Goal.get_or_none(Goal.id == goal_id)
    if not goal:
        return "Goal not found", 404

    workouts = Workout.select().where(Workout.user == goal.user).order_by(Workout.date)
    dates = [workout.date for workout in workouts]
    progress = [sum(1 for _ in workouts if _.date <= date) for date in dates]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=progress, mode='lines+markers', name='Progress'))
    fig.update_layout(
        title=f"Progress for Goal: {goal.description}",
        xaxis_title="Date",
        yaxis_title="Cumulative Progress",
        template="plotly_dark"
    )

    return render_template('line_chart.html', chart=fig.to_html(full_html=False), goal=goal)
