#!/usr/bin/env python3
"""implementing authentication class for our RestApi."""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """initializing class auth."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a given path requires authorization"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            normalized_path = path.rstrip('/') + '/'
            normalized_excluded_path = excluded_path.rstrip('/') + '/'
            if normalized_path == normalized_excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """creating an authorization header instance."""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """checks for a currently authenicated user."""
        return None

    def session_cookie(self, request=None):
        """return a cookie session from request."""
        session_name = os.environ.get('SESSION_NAME', '_my_session_id')
        if request is None:
            return None

        cookie_value: str = request.cookies.get(session_name)

        return cookie_value
