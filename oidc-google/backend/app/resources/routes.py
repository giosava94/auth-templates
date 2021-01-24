"""
Define routes with application endpoints.

savarese.giovanni94@gmail.com
"""

from .endpoints import Private, Public


def add_generic_routes(api):
    api.add_resource(Private, "/api/private")
    api.add_resource(Public, "/api/public")