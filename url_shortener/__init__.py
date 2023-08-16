from flask import Flask
from .extensions import db, bcrypt
from .routes import shortener
from flask_login import LoginManager
from .models import User

login_manager = LoginManager()  # Create the LoginManager instance
# login_manager.unauthorized_view = 'shortener.login_user'  # Redirect to the login page
# login_manager.login_view = 'shortener.login_user'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'shortener.login_user'
    app.register_blueprint(shortener)
    with app.app_context():
        db.create_all()
    return app
