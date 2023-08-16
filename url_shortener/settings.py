import secrets
import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'

SQLALCHEMY_TRACK_NOTIFICATIONS = False
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

SECRET_KEY = 'your_secret_key_here'
