"""
Start flask app adding authentication routes.

The import of authentication routes is based on a environment macro in order to
allow custom imports without the need to modify this file.

savarese.giovanni94@gmail.com
"""

import importlib
from app import app, api, socketio
from app.socket.generic import add_generic_handlers
from app.config import AUTH_TYPE, AUTH_ENABLED

add_generic_handlers(socketio)

if AUTH_ENABLED:
    try:
        # User desired authentication method.
        # Import based on module name.
        add_auth_routes = importlib.import_module(
            "app.auth.providers." + AUTH_TYPE
        ).add_auth_routes
    except:
        # Standard authentication when the specified authentication
        # does not exists or it is not specified
        from app.auth.providers.local import add_auth_routes

    add_auth_routes(api)

if __name__ == "__main__":
    socketio.run(app, debug=True)