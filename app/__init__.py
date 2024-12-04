from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import db, User

bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))  # Fetch user by ID

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
    app.config['DATABASE'] = 'fitness_app.db'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Set up login manager
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .routes import main
    from .auth import auth  # Authentication blueprint
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
