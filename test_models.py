import os
from app.models import db, User, Goal, Workout
from app import bcrypt

def populate_test_data():
    # Initialize the database
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'databases', 'fitness_app.db')
    db.init(db_path)  # Link the db object to the correct database file
    db.connect()

    # Create tables if they don't already exist
    db.create_tables([User, Goal, Workout], safe=True)

    # Create some test users with hashed passwords
    hashed_password1 = bcrypt.generate_password_hash("testpassword1").decode('utf-8')
    hashed_password2 = bcrypt.generate_password_hash("testpassword2").decode('utf-8')

    user1 = User.create(username="testuser1", email="test1@example.com", password=hashed_password1)
    user2 = User.create(username="testuser2", email="test2@example.com", password=hashed_password2)

    # Add test goals for user1
    Goal.create(user=user1.id, description="Run 50 miles in a month", target_date="2024-12-31", target_value=50)
    Goal.create(user=user1.id, description="Lift 5000 lbs in a week", target_date="2024-12-15", target_value=5000)

    # Add test workouts for user1
    Workout.create(user=user1.id, workout_type="run", date="2024-12-01", duration=60, intensity=None, exercise=None, weight=None, sets=None)
    Workout.create(user=user1.id, workout_type="weightlifting", date="2024-12-02", duration=None, intensity=None, exercise="bench_press", weight=200, sets=5, reps=3)

    # Print success message
    print("Test data populated successfully!")

    # Close the database connection
    db.close()

if __name__ == "__main__":
    populate_test_data()
