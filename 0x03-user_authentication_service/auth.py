#!/usr/bin/env python3
"""This module contains all functions and classes to manage authentication."""

import bcrypt
import uuid
from user import User
from typing import Union, TypeVar
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """create a password hash that returns the password hash.
    """
    salt = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """generates anique identifier"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """initializing a storage instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user to the database."""
        if isinstance(email, str) and isinstance(password, str):
            try:
                user: TypeVar('User') = self._db.find_user_by(email=email)
                raise ValueError(f"User {email} already exists")

            except NoResultFound:
                hashed_password: bytes = _hash_password(password)
                registered_user: TypeVar('user') = \
                self._db.add_user(email, hashed_password)
                return registered_user

    def valid_login(self, email: str, password: str) -> bool:
        """check if a given login is valid."""
        if isinstance(email, str) and isinstance(password, str):
            try:
                user: TypeVar('User') = self._db.find_user_by(email=email)
                hashed_password = user.hashed_password
                return bcrypt.checkpw(password.encode('utf-8'),
                                      hashed_password)
            except NoResultFound:
                return False

    def create_session(self, email: str) -> str:
        """creates a user session."""
        assert type(email) is str
        try:
            user: TypeVar('User') = self._db.find_user_by(email=email)
            session_id: str = _generate_uuid()
            user.session_id = session_id
            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[TypeVar('User'), None]:
        """gets a user from a session_id"""
        if session_id is None:
            return None
        try:
            user: TypeVar('User') = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(user_id: str) -> None:
        """destroys a user's session."""
        assert type(user_id) is str
        try:
            user: TypeVar('User') = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except (ValueError, NoResultFound):
            return None

    def get_reset_password_token(email: str) -> str:
        """Create a password reset token."""
        assert type(email) is str
        try:
            user: User = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(reset_token: str, password: str) -> None:
        """Changes a user's password."""
        assert type(reset_token) is str and type(password) is str
        try:
            user: User = self._db.find_user_by(reset_token=reset_token)
            new_hashed_password = self._hashed_password(password)
            user.hashed_password = new_hashed_password
            user.reset_token = None
            return None
        except NoResultFound:
            raise ValueError
