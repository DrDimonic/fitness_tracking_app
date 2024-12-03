from flask import Flask
from peewee import SqliteDatabase

db = SqliteDatabase('fitness_tracker.db')

# Initialize the app withe key
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    from .routes import main
    app.register_blueprint(main)

    return app
