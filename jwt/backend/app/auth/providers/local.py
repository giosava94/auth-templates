"""
Local authentication and authorization.

It shows and example logic with some basic implementation.

savarese.giovanni94@gmail.com
"""

from flask_restful import Resource, abort
from webargs import fields
from webargs.flaskparser import use_args
from ..user import Logout, Refresh, get_tokens


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

        # Attache JWT tokens to the response
        user_data = {"id": username, "username": username, "groups": groups}
        resp = get_tokens(user_data)

        return resp