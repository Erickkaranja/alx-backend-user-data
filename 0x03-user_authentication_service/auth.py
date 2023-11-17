#!/usr/bin/env python3
""""""
import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> str:
    """"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def _generate_uuid():
    """
    """
    gen_id = str(uuid.uuid4())
    return gen_id

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """
        """
        try:
            hashed_password = _hash_password(password)
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")

        except NoResultFound:
            registered_user = self._db.add_user(email, hashed_password)
            return registered_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(session_id):
        """
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(user_id: int):
        """
        """
        try:
            user = self._db.find_user_by(user_id=user_id)
            user.session_id = None
            return None
        except:
            return None

    def get_reset_password_token(email: str) -> str:
        """
        """
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError
        reset_token = str(uuuid.uuid4())
        user.reset_token = reset_token
        return reset_token

    def update_password(reset_token: str, password: str):
        """
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError
        new_hashed_password = self._hashed_password(password)
        user.hashed_password = new_hashed_password
        user.reset_token = None
        return None
