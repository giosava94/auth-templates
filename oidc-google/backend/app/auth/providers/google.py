"""
Custom authentication using the GOOGLE OpenIDConnect provider.

It uses the standard Logout and Refresh resources, whereas it implements its
own flow for the sing-in procedure.

savarese.giovanni94@gmail.com
"""

import json, requests, os
from oauthlib.oauth2 import WebApplicationClient
from flask import request
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from ..user import Login, Logout, get_tokens

# Configuration
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
SECRET = os.environ.get("GOOGLE_SECRET", None)
DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth 2 client setup
client = WebApplicationClient(CLIENT_ID)

# Mapping local key value with external site key value
keywords = {
    "username": "given_name",
    "picture": "picture",
    "email": "email",
    "uuid": "sub",
}


def add_auth_routes(api):
    api.add_resource(ProviderAuthorization, "/api/auth-url")
    api.add_resource(Login, "/api/login")
    api.add_resource(Logout, "/api/logout")
    api.add_resource(Refresh, "/api/refresh")


def get_authz_url(args):
    """
    Find out what URL to hit for provider login

    Use library to construct the request for provider login and provide
    scopes that let you retrieve user's profile from the provider
    """

    provider_cfg = requests.get(DISCOVERY_URL).json()
    authorization_endpoint = provider_cfg["authorization_endpoint"]

    return client.prepare_request_uri(authorization_endpoint, **args)


def get_token_from_code(request):
    """
    Get authorization code the provider sent back to you

    Find out what URL to hit to get tokens that allow you to ask for
    things on behalf of a user.

    Prepare and send a request to get tokens.

    Parse the tokens using the OAuth 2 client
    """

    code = request.args.get("code")
    redirect_uri = request.args.get("redirect_uri")

    provider_cfg = requests.get(DISCOVERY_URL).json()
    token_endpoint = provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=redirect_uri,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(CLIENT_ID, SECRET),
    )

    token_response = token_response.json()

    client.parse_request_body_response(json.dumps(token_response))

    return token_response


def get_user_info(fields):
    """
    Now that you have tokens (yay) let's find and hit the URL
    from the provider that gives you the user's profile information,
    including their profile image and email
    """

    provider_cfg = requests.get(DISCOVERY_URL).json()
    userinfo_endpoint = provider_cfg["userinfo_endpoint"]

    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo_response = userinfo_response.json()

    if userinfo_response.get("email_verified"):
        data = {}
        for field in fields:
            val = userinfo_response.get(keywords[field], None)
            if not (val is None):
                data[field] = val
        return data
    else:
        return "User email not available or not verified.", 400


def get_groups(username):
    """
    Return the list of groups the user belongs to.
    """
    return []


class ProviderAuthorization(Resource):
    """
    Get the correct link to redirect the client
    to perform the login with an external provider.
    """

    args = {
        "redirect_uri": fields.Str(),
        "scope": fields.Str(),
        "login_hint": fields.Str(),
        "prompt": fields.Str(),
        "access_type": fields.Str(),
    }

    @staticmethod
    @use_args(args, location="query")
    def get(args):
        scope = args.get("scope", None)
        if not (scope is None):
            args["scope"] = scope.split()

        return get_authz_url(args)


class Login(Resource):
    """
    API Resource to perform login using the code received
    from the trusted provider, retrieve a set of
    user information and create new local JWT tokens
    (access and refresh ones).
    """

    args = {
        "redirect_uri": fields.Str(),
        "scope": fields.Str(),
        "code": fields.Str(),
        # List of user information to get from the provider.
        # The list is a string where list items are separated by a blank space.
        "user_details": fields.Str(),
    }

    @staticmethod
    @use_args(args, location="query")
    def get(args):
        user_details = args.get("user_details", None)
        if not (user_details is None):
            user_details = user_details.split()

        token_info = get_token_from_code(request)
        user_data = get_user_info(user_details)

        # Here the user is authenticated
        # We need to extract only relevant information for this app.
        # Retrieved information can be used to extract data from a local DB,
        # for example retrieve groups from a local DB
        user_data["groups"] = get_groups(user_data["username"])

        # Attache JWT tokens to the response
        resp = get_tokens(user_data)

        return resp
