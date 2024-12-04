from peewee import Model, SqliteDatabase, CharField, DateField, IntegerField
from flask_login import UserMixin

# Define the database object
db = SqliteDatabase(None)  # Database initialization will happen later

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel, UserMixin):
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True)
    password = CharField()

class Goal(BaseModel):
    user = IntegerField()  # Replace with ForeignKeyField(User, backref="goals") if using relationships
    description = CharField()
    target_date = DateField()
    target_value = IntegerField()

class Workout(BaseModel):
    user = IntegerField()  # Replace with ForeignKeyField(User, backref="workouts") if using relationships
    workout_type = CharField()
    date = DateField()
    duration = IntegerField(null=True)  # For runs
    intensity = CharField(null=True)   # For runs
    exercise = CharField(null=True)    # For weightlifting
    weight = IntegerField(null=True)   # For weightlifting
    sets = IntegerField(null=True)     # For weightlifting
