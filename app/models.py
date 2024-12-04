from peewee import Model, CharField, DateField, IntegerField, ForeignKeyField
from . import db

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class Goal(Model):
    user = ForeignKeyField(User, backref='goals')
    description = CharField()
    target_date = DateField()
    target_value = IntegerField()

    class Meta:
        database = db

class Workout(Model):
    user = ForeignKeyField(User, backref='workouts')
    workout_type = CharField()
    date = DateField()
    duration = IntegerField(null=True)  # For runs
    intensity = CharField(null=True)   # For runs
    exercise = CharField(null=True)   # For weightlifting
    weight = IntegerField(null=True)  # For weightlifting
    sets = IntegerField(null=True)    # For weightlifting

    class Meta:
        database = db