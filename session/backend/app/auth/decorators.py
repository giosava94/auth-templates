"""
Decorators to manage authentication and authorization.

savarese.giovanni94@gmail.com
"""

import functools
from flask_login import current_user
from flask_socketio import disconnect
from ..config import AUTH_ENABLED


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if AUTH_ENABLED and not current_user.is_authenticated:
            print("User is not authenticated")
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


def authorized_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if AUTH_ENABLED:
            print(current_user.groups)
        # if not set(current_user.groups).intersection(set(authorized)):
        #    # User not authorized
        #    return  # TODO return what?
        # else:
        #    return f(*args, **kwargs)
        return f(*args, **kwargs)

    return wrapped
