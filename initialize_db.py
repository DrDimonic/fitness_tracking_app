from app.models import db, User, Workout, Goal

# Script to create and initialize the database
def initialize_database():
    db.connect()
    db.create_tables([User, Goal, Workout], safe=True)
    print("Database initialized successfully.")
    db.close()

if __name__ == '__main__':
    initialize_database()
