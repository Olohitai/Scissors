from functools import wraps
from flask import request, Response, current_app, redirect, url_for
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, LoginManager, UserMixin
from .models import User, db


login_manager = LoginManager()
login_manager.login_view = 'shortener.login_user'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def register(email, username, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False, "Email already registered"

    new_user = User(username=username, email=email,
                    password=password)  # Update this line
    db.session.add(new_user)
    db.session.commit()
    return True, "Registration successful"


def login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return True, "Login successful"
    return False, "Please check your login details and try again."
