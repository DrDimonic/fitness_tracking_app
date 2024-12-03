from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class WorkoutForm(FlaskForm):
    workout_type = StringField('Workout Type', validators=[DataRequired(), Length(max=50)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    duration = SelectField(
        'Duration (minutes)',
        choices=[(str(i), f"{i} minutes") for i in range(5, 121, 5)],  # Dropdown: 5 to 120 minutes
        validators=[DataRequired()]
    )
    intensity = StringField('Intensity', validators=[DataRequired(), Length(max=20)])
    notes = StringField('Notes', validators=[Length(max=200)])
    submit = SubmitField('Log Workout')

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

