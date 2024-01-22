#!/usr/bin/env python3
"""implimenting authentication session routes."""

from typing import TypeVar
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os

SESSION_NAME = os.getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """implementing a session login."""
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        user: TypeVar('User') = User.search({'email': email})[0]
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = str(auth.create_session(user.id))
            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401

    except IndexError:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """implements a session logout."""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
