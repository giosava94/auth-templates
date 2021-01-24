"""
Generic private and public endpoints.

savarese.giovanni94@gmail.com
"""

from flask_restful import Resource
from flask_jwt_extended import jwt_required


class Private(Resource):
    """
    Private get route.
    Use jwt_required decorator to validate JWTs.
    """

    @staticmethod
    @jwt_required
    def get():
        """
        Return a message
        """

        return {"data": "private"}


class Public(Resource):
    """
    Public get route.
    """

    @staticmethod
    def get():
        """
        Return a message
        """

        return {"data": "public"}
