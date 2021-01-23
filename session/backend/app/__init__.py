"""
Flask app initialization.

savarese.giovanni94@gmail.com
"""

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_session import Session
from .config import FlaskConfig
from .auth.user import User

# Flask app initialisation
app = Flask(__name__)
app.config.from_object(FlaskConfig())
api = Api(app)
CORS(app)
login_manager = LoginManager(app)
Session(app)
socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*", logger=True)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)