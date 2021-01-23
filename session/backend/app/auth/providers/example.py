"""
User custom authentication and authorizations endpoints.

Use this file and `local.py` as reference.

The implementation of the `add_auth_routes()` function is mandatory.
There you can add all needed resources.

If you implement a custom login procedure remember to use the
`start_user_session` function of the standard procedure. 
It is mandatory in order to start the user session using Flask-Login.
We already import that function for you.
(`from ..user import start_user_session`)

If you want to implement one Resource and re-use an existing one 
you can import the resource from the correct module and link the 
correct endpoint.

Remember that these endpoints and these resources will overwrite the
existing ones.

savarese.giovanni94@gmail.com
"""

from ..user import start_user_session


def add_auth_routes(api):
    # Add here API resources and corresponding endpoints.
    # Here an example:
    #
    # api.add_resource(Login, "/api/login")
    pass
