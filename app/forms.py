from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class SelectWorkoutTypeForm(FlaskForm):
    workout_type = SelectField(
        'Select Workout Type',
        choices=[('run', 'Running'), ('weightlifting', 'Weightlifting')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Next')

class RunForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    distance = FloatField('Distance (miles)', validators=[DataRequired()])
    time = FloatField('Time (minutes)', validators=[DataRequired()])
    submit = SubmitField('Log Run')

class WeightliftingForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    exercise = SelectField(
        'Exercise',
        choices=[
            ('bench_press', 'Bench Press'),
            ('squat', 'Squat'),
            ('deadlift', 'Deadlift'),
            ('overhead_press', 'Overhead Press'),
            ('custom', 'Custom')
        ],
        validators=[DataRequired()]
    )
    custom_exercise = StringField('Custom Exercise Name', validators=[Optional(), Length(max=50)])
    weight = FloatField('Weight (lbs)', validators=[DataRequired()])
    sets = IntegerField('Number of Sets', validators=[DataRequired()])
    difficulty = SelectField(
        'Difficulty',
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Log Weightlifting')

class GoalForm(FlaskForm):
    goal_description = StringField('Goal Description', validators=[DataRequired(), Length(max=100)])
    target_date = DateField('Target Date', format='%Y-%m-%d', validators=[DataRequired()])
    target_value = SelectField(
        'Target Value',
        choices=[(str(i), f"{i} days") for i in range(1, 31)] +  # 1-30 days
                [(str(i), f"{i} weeks") for i in range(1, 53)] +  # 1-52 weeks
                [(str(i), f"{i} months") for i in range(1, 13)],  # 1-12 months
        validators=[DataRequired()]
    )
    submit = SubmitField('Set Goal')

