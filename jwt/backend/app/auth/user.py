"""
Define resources for authentication and authorization access control.

savarese.giovanni94@gmail.com
"""

from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)


def get_tokens(current_user, refresh=True):
    """
    Create the tokens we will be sending back to the user
    Set the JWTs and the CSRF double submit protection cookies
    in this response
    """

    access_token = create_access_token(identity=current_user, fresh=True)
    resp = jsonify(current_user)
    set_access_cookies(resp, access_token)

    if refresh:
        refresh_token = create_refresh_token(identity=current_user)
        set_refresh_cookies(resp, refresh_token)

    return resp


class Refresh(Resource):
    """
    API Resource to refresh the access token
    """

    @staticmethod
    @jwt_refresh_token_required
    def get():
        current_user = get_jwt_identity()
        return get_tokens(current_user, refresh=False)


class Logout(Resource):
    """
    API Resource to logout the user and clear cookies
    """

    @staticmethod
    def get():
        resp = jsonify(True)
        unset_jwt_cookies(resp)
        return resp