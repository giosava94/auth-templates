"""
Local authentication and authorization provider.

It shows and example logic with some basic implementation.

savarese.giovanni94@gmail.com
"""

from flask_restful import Resource, abort
from flask_login import logout_user, current_user
from webargs import fields
from webargs.flaskparser import use_args
from ..user import User, start_user_session


def add_auth_routes(api):
    api.add_resource(Login, "/api/login")
    api.add_resource(Logout, "/api/logout")
    api.add_resource(Refresh, "/api/refresh")


def check_password(password):
    """
    Validate password
    """

    return True


def check_username(username):
    """
    Validate user
    """

    return True


def get_groups(username):
    """
    From the username (unique identifier) get authorized groups
    """

    return []


class Login(Resource):
    """
    Standard Login Resource
    """

    args = {
        "username": fields.Str(required=True, allow_none=False),
        "password": fields.Str(required=True, allow_none=False),
    }

    @staticmethod
    @use_args(args)
    def post(args):
        username = args["username"]
        password = args["password"]

        # Authentication procedure
        if not check_username(username):
            abort(401)
        if not check_password(password):
            abort(401)

        # Retrieve groups from a local DB
        groups = get_groups(username)

        # Start user session using Flask-Login
        user_data = {"id": username, "username": username, "groups": groups}
        start_user_session(user_data)

        return user_data


class Logout(Resource):
    """
    Logout user and clear user session
    """

    @staticmethod
    def get():
        logout_user()
        return True


class Refresh(Resource):
    """
    Check if user is already logged in.
    """

    @staticmethod
    def get():
        if current_user.is_authenticated:
            user_data = {
                "id": current_user.id,
                "username": current_user.name,
                "groups": current_user.groups,
            }
            return user_data
        else:
            return None