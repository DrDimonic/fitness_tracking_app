from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class WorkoutForm(FlaskForm):
    workout_type = StringField('Workout Type', validators=[DataRequired(), Length(max=50)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    intensity = StringField('Intensity', validators=[DataRequired(), Length(max=20)])
    notes = StringField('Notes', validators=[Length(max=200)])
    submit = SubmitField('Log Workout')
    
class GoalForm(FlaskForm):
    goal_description = StringField('Goal Description', validators=[DataRequired(), Length(max=100)])
    target_date = DateField('Target Date', format='%Y-%m-%d', validators=[DataRequired()])
    target_value = IntegerField('Target Value (e.g., minutes or sessions)', validators=[DataRequired()])
    submit = SubmitField('Set Goal')
