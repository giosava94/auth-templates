"""
Socket main handlers.

To check user authentication and authorizations it uses the decorators
in the auth package. User authentication is not required after the connection
has been established but it can be useful in some cases.

savarese.giovanni94@gmail.com
"""

from flask import request
from flask_socketio import emit, disconnect
from flask_login import current_user
from ..auth.decorators import authenticated_only, authorized_only
from ..config import AUTH_ENABLED


@authenticated_only
def handle_connection():
    if AUTH_ENABLED:
        print("Client %s connected as user %s", request.sid, current_user.id)
    else:
        print("Client %s connected", request.sid)


def handle_disconnection():
    disconnect()
    print("Client %s disconnected", request.sid)


@authorized_only
def handle_custom_event(data):
    print("my_event data %s", data)
    emit("my_response", {"data": "test"})


def add_generic_handlers(socketio):
    """
    Attach handlers to the socketio instance
    """

    socketio.on_event("connect", handle_connection)
    socketio.on_event("disconnect", handle_disconnection)
    socketio.on_event("my_event", handle_custom_event)