from .extensions import db, bcrypt
from datetime import datetime
import string
from random import choices
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(1024))
    short_url = db.Column(db.String(6), unique=True)
    views = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = "".join(choices(characters, k=6))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()

        return short_url

 # User MOdel


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password):  # Update this line
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

      # Implement UserMixin methods
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
