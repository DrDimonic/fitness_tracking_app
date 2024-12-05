from app.models import db, User, Workout, Goal
from app import bcrypt
from datetime import date
import os


def populate_test_data():
    # Initialize the database
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'databases', 'fitness_app.db')
    db.init(db_path)  # Link the db object to the correct database file
    db.connect()

    # Drop tables and recreate them for a clean slate
    db.drop_tables([User, Workout, Goal], safe=True)
    db.create_tables([User, Workout, Goal])

    # Create test users
    user1 = User.create(
        username="testuser1",
        email="test1@example.com",
        password=bcrypt.generate_password_hash("password1").decode("utf-8")
    )
    user2 = User.create(
        username="testuser2",
        email="test2@example.com",
        password=bcrypt.generate_password_hash("password2").decode("utf-8")
    )

    # Create goals for user1
    Goal.create(
        user=user1.id,
        description="Run 50 miles in December",
        target_date="2024-12-31"
    )
    Goal.create(
        user=user1.id,
        description="Lift 10,000 lbs this week",
        target_date="2024-12-10"
    )
    Goal.create(
        user=user1.id,
        description="Workout 15 times this month",
        target_date="2024-12-31"
    )

    # Add workouts for user1
    Workout.create(
        user=user1.id,
        workout_type="run",
        date=date(2024, 12, 1),
        distance=5,  # miles
        duration=50  # minutes
    )
    Workout.create(
        user=user1.id,
        workout_type="run",
        date=date(2024, 12, 2),
        distance=8,  # miles
        duration=60  # minutes
    )
    Workout.create(
        user=user1.id,
        workout_type="weightlifting",
        date=date(2024, 12, 3),
        exercise="bench_press",
        weight=200,
        sets=5,
        reps=10,
        duration=30  # minutes
    )
    Workout.create(
        user=user1.id,
        workout_type="weightlifting",
        date=date(2024, 12, 4),
        exercise="squat",
        weight=250,
        sets=4,
        reps=8,
        duration=45  # minutes
    )

    # Add workouts for user2
    Workout.create(
        user=user2.id,
        workout_type="run",
        date=date(2024, 12, 5),
        distance=6,  # miles
        duration=55  # minutes
    )
    Workout.create(
        user=user2.id,
        workout_type="weightlifting",
        date=date(2024, 12, 6),
        exercise="deadlift",
        weight=300,
        sets=3,
        reps=5,
        duration=40  # minutes
    )

    print("Test data populated successfully!")

    # Close the database connection
    db.close()


if __name__ == "__main__":
    populate_test_data()
