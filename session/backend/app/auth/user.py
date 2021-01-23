"""
User class to manage user session.

savarese.giovanni94@gmail.com
"""

import json, os
from flask_login import UserMixin, login_user


class User(UserMixin):
    def __init__(self, id_, name, groups):
        self.id = id_
        self.name = name
        self.groups = groups

    @staticmethod
    def get(user_id):
        with open("users.txt", "r") as users_file:
            users = json.load(users_file)
        user = users.get(user_id, None)
        if not (user is None):
            return User(
                id_=user_id,
                name=user.get("name", None),
                groups=user.get("groups", None),
            )
        else:
            return None

    @staticmethod
    def create(id_, name, groups):
        f_name = "users.txt"
        users = {}

        if not os.path.isfile(f_name):
            with open(f_name, "w") as users_file:
                json.dump(users, users_file)

        with open(f_name, "r") as users_file:
            users = json.load(users_file)

        users[id_] = {"name": name, "groups": groups}
        with open(f_name, "w") as users_file:
            json.dump(users, users_file)


def start_user_session(user_data):
    """
    Start user session using Flask-Login
    """

    username = user_data.get("username", None)
    groups = user_data.get("groups", None)
    id_ = user_data.get("id", None)
    # TODO: Manage when they are None

    # Create a user with provided information
    user = User(id_, username, groups)

    # Doesn't exist? Create it.
    if not User.get(id_):
        User.create(id_, username, groups)

    # Begin user session by logging the user in
    login_user(user)
