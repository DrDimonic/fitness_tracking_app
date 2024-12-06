from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import db, User, Goal, Workout
from .routes import main
import os

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    # Load user by ID for login session management
    return User.get_or_none(User.id == int(user_id))

# Create and configure the Flask app
def create_app(): 
    app = Flask(__name__)

    # Application configurations
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'databases', 'fitness_app.db')

    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Default view for unauthorized access
    login_manager.login_view = 'auth.login' 

    # Initialize database
    db.init(app.config['DATABASE'])

    # Create tables if they don't already exist
    with db:
        db.create_tables([User, Goal, Workout])

    # Register Blueprints
    from .authenticate import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
