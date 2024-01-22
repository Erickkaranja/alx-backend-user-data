#!/usr/bin/env python3
"""instanciating a session authentication for a user."""
from typing import TypeVar
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """instanciating class SessionAuth."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creating a user session."""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrives the user object based on session_id."""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id: str = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """returns current use by session id."""
        cookie_value: str = self.session_cookie(request)
        user_id: str = self.user_id_for_session_id(cookie_value)
        user: TypeVar('User') = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """destroys the current session / logout."""
        if request is None:
            return False
        session_id: str = self.session_cookie(request)
        if session_id is None:
            return False
        user_id: str = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        else:
            del self.user_id_by_session_id[session_id]
            return True
