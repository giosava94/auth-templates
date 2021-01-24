"""
Flask app initialization.

savarese.giovanni94@gmail.com
"""

import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import ConfigJWT, ConfigCors

# Flask app initialisation
app = Flask(__name__)
app.config.from_object(ConfigJWT())
app.config.from_object(ConfigCors())
CORS(app)
JWTManager(app)
api = Api(app)