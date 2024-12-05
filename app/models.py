from peewee import Model, SqliteDatabase, CharField, DateField, IntegerField, FloatField, ForeignKeyField
from flask_login import UserMixin

# Define the database object
db = SqliteDatabase(None)  # Database initialization will happen later



class User(Model, UserMixin):
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class Goal(Model):
    user = IntegerField()  
    description = CharField()
    target_date = DateField()

    class Meta:
        database = db

class Workout(Model):
    user = ForeignKeyField(User, backref='workouts')
    workout_type = CharField()  # 'run' or 'weightlifting'
    date = DateField()
    distance = FloatField(null=True)  # Allow NULL for non-running workouts
    duration = FloatField(null=True)  # Duration in minutes
    exercise = CharField(null=True)  # Specific to weightlifting
    weight = FloatField(null=True)
    sets = IntegerField(null=True)
    reps = IntegerField(null=True)

    class Meta:
        database = db
