from app.models import db, User, Goal, Workout
import os

def initialize_database():
    # Define the database path
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'databases', 'fitness_app.db')

    # Initialize the database
    db.init(db_path)
    db.connect()

    # Create tables if they don't exist
    db.create_tables([User, Goal, Workout], safe=True)
    print("Database initialized successfully.")

    # Close the database connection
    db.close()

if __name__ == '__main__':
    initialize_database()
