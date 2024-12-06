from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import db, User
from .routes import main
import os

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()

# Load user by ID for login session management
@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))  

# Create and configure the Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Application configurations
    app.config['SESSION_PROTECTION'] = 'strong'  
    app.config['REMEMBER_COOKIE_DURATION'] = 0  

    
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
