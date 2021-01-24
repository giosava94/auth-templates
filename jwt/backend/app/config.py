"""
Configuration details:
    Flask:
        CORS
        JWT-Extended
    Auth:
        Authentication type
        Authorization file matching

savarese.giovanni94@gmail.com
"""

import os
from random import choice
from string import ascii_letters, digits
from datetime import timedelta
from distutils.util import strtobool

# User defined authentication type
AUTH_ENABLED = strtobool(os.environ.get("REACT_APP_AUTH_ENABLED", "false"))
AUTH_TYPE = os.environ.get("REACT_APP_AUTHN", "").lower()

# Path to the local authorization file
AUTHORIZATIONS_FILE = "../users/authorizations.json"

# Configuration object with relevant variables.
class ConfigJWT(object):
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    if JWT_SECRET_KEY == None or JWT_SECRET_KEY == "":
        JWT_SECRET_KEY = "".join(choice([ascii_letters, digits]) for i in range(12))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_PATH = "/api/"
    JWT_ACCESS_CSRF_COOKIE_PATH = "/api/"
    JWT_REFRESH_COOKIE_PATH = "/api/refresh"
    JWT_REFRESH_CSRF_COOKIE_PATH = "/api/refresh"
    JWT_COOKIE_SECURE = strtobool(os.environ.get("JWT_COOKIE_SECURE", "False"))
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_IN_COOKIES = True
    JWT_CSRF_METHODS = []


# Configuration object with relevant variables.
class ConfigCors(object):
    CORS_RESOURCES = [r"/api/*"]
    CORS_SUPPORTS_CREDENTIALS = True
