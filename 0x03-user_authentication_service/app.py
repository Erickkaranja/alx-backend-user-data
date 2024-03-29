#!/usr/bin/env python3
"""Creating a flask application instance."""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index() -> str:
    """ creating a welcome message."""

    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'], strict_slashes=False)
def user():
    """Add a new user to the database."""
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    try:
        registered = AUTH.register_user(email, password)
        return jsonify({"email": registered.email,
                        "message": "user created"})
    except ValueError:
        message = {"message": "email already registered"}
        return jsonify(message), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Handle user's sign in functionality."""
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logout a user."""
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except AttributeError:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Returns a user profile."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Get a pass word reset token."""
    email: str = request.form['email']
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """update's a user's pasword."""
    email: str = request.form.get('email')
    reset_token: str = request.form.get('reset_token')
    new_password: str = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
