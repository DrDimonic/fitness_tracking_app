from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import SelectWorkoutTypeForm, RunForm, WeightliftingForm, GoalForm

# Blueprint for the main routes
main = Blueprint('main', __name__)

# Render homepage template
@main.route('/')
def index():
    return render_template('index.html')

# Route for logging workouts
@main.route('/log_workout', methods=['GET', 'POST'])
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
        difficulty = lifting_form.difficulty.data

        # Calculate calories burned (example logic)
        difficulty_multiplier = {'easy': 3, 'moderate': 5, 'hard': 8}
        calories_burned = sets * weight * difficulty_multiplier[difficulty]

        # Save to database (example only)
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