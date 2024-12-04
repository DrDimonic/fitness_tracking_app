from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
    app.config['DATABASE'] = 'fitness_app.db'

    # Initialize extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models and register blueprints here to prevent circular imports
    from .models import db, User
    db.init_app(app)

    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
