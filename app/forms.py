from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional
from . import db

class SelectWorkoutTypeForm(FlaskForm):
    workout_type = SelectField(
        choices=[('run', 'Running'), ('weightlifting', 'Weightlifting')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Next')

class RunForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    distance = FloatField('Distance (miles)', validators=[DataRequired()])
    duration = FloatField('Time (minutes)', validators=[DataRequired()])
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
            ('pull_up', 'Pull-Up'),
            ('chin_up', 'Chin-Up'),
            ('barbell_row', 'Barbell Row'),
            ('dumbbell_row', 'Dumbbell Row'),
            ('lat_pulldown', 'Lat Pulldown'),
            ('incline_bench_press', 'Incline Bench Press'),
            ('dumbbell_curl', 'Dumbbell Curl'),
            ('barbell_curl', 'Barbell Curl'),
            ('tricep_dip', 'Tricep Dip'),
            ('skull_crusher', 'Skull Crusher'),
            ('leg_press', 'Leg Press'),
            ('lunges', 'Lunges'),
            ('romanian_deadlift', 'Romanian Deadlift'),
            ('calf_raise', 'Calf Raise'),
            ('seated_calf_raise', 'Seated Calf Raise'),
            ('leg_extension', 'Leg Extension'),
            ('leg_curl', 'Leg Curl'),
            ('shoulder_press', 'Shoulder Press'),
            ('side_lateral_raise', 'Side Lateral Raise'),
            ('face_pull', 'Face Pull'),
            ('custom', 'Custom')  # Allows custom exercise entry
        ],
        validators=[DataRequired()]
    )
    custom_exercise = StringField('Custom Exercise Name', validators=[Optional(), Length(max=50)])
    weight = FloatField('Weight (lbs)', validators=[DataRequired()])
    sets = IntegerField('Number of Sets', validators=[DataRequired()])
    reps = IntegerField('Repetitions', validators=[DataRequired()])  # New field for repetitions
    difficulty = SelectField(
        'Difficulty',
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Log Weightlifting')

class GoalForm(FlaskForm):
    goal_description = StringField('Goal Description', validators=[DataRequired(), Length(max=100)])
    target_date = DateField('Target Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Set Goal')

