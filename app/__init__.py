from flask import Flask
from peewee import SqliteDatabase

# Initialize the database connection with Peewee ORM
db = SqliteDatabase('fitness_tracker.db')

# Create the flask application instance and create the key
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Import and register the blueprint for routes
    from .routes import main
    app.register_blueprint(main)

    return app
