from app.models import db, User, Goal, Workout
import os

# Initialize the database and create tables if they don't already exist
def initialize_database():
    db_path = os.path.join(os.path.dirname(__file__), 'app', 'databases', 'fitness_app.db')

    db.init(db_path)
    db.connect()
    db.create_tables([User, Goal, Workout], safe=True)
    print("Database initialized successfully.")
    db.close()

if __name__ == '__main__':
    initialize_database()
