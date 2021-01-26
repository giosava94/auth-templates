"""
Configuration details:
    Flask:
        CORS
        Session
    Auth:
        Authentication type
        Authorization file matching

savarese.giovanni94@gmail.com
"""

import os
from random import choice
from string import ascii_letters, digits
from distutils.util import strtobool

# User defined authentication type
AUTH_ENABLED = strtobool(os.environ.get("REACT_APP_AUTH_ENABLED", "false"))
AUTH_TYPE = os.environ.get("REACT_APP_AUTHN", "").lower()

# Path to the local authorization file
AUTHORIZATIONS_FILE = "../users/authorizations.json"
USERS_DB_FILE = "users.txt"

if AUTH_ENABLED and not os.path.isfile(USERS_DB_FILE):
    with open(USERS_DB_FILE, "w") as f:
        f.write("{}")


# Configuration object with relevant variables.
class FlaskConfig(object):
    # CORS
    CORS_RESOURCES = [r"/api/*"]
    CORS_SUPPORTS_CREDENTIALS = True

    # SESSION
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if SECRET_KEY == None or SECRET_KEY == "":
        SECRET_KEY = "".join(choice([ascii_letters, digits]) for i in range(12))
    SESSION_TYPE = "filesystem"
