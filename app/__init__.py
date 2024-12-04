from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import db, User

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DATABASE'] = 'fitness_app.db'

    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize the database
    db.init(app.config['DATABASE'])

    # Create tables
    with db:
        db.create_tables([User, Goal, Workout])

    # Register blueprints
    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
