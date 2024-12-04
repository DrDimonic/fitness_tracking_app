from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import db, User
import os

bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))  # Fetch the user by ID from the database

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Set the database path
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'databases', 'fitness_app.db')

    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize the database
    db.init(app.config['DATABASE'])

    # Register blueprints
    from .routes import main
    from .authenticate import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
