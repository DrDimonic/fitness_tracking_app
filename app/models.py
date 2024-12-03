from peewee import Model, CharField, DateField, IntegerField, ForeignKeyField
from . import db

# Base model from which all other models will inherit
class BaseModel(Model):
    class Meta:
        database = db

# Model to store user account information
class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

# Workout model to log individual workout details
class Workout(BaseModel):
    user = ForeignKeyField(User, backref='workouts')
    workout_type = CharField()
    date = DateField()
    duration = IntegerField()  # Minutes
    intensity = CharField()
    notes = CharField(null=True)

# Model for user goal setting
class Goal(BaseModel):
    user = ForeignKeyField(User, backref='goals')
    description = CharField()
    target_date = DateField()
    target_value = IntegerField()
    progress = IntegerField(default=0)
