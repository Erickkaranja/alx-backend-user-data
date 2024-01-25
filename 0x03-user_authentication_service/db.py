#!/usr/bin/env python3
"""implementing DB class reptesenting database session.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """creating a new user object by email and password.
           Args:
               email (str): user email.
               hashed_password (str): user password.
           Returns:
               User (TypeVar('user')): a user object.
        """
        new_user: TypeVar('User') = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """finding user by passed keyword arguements passed.
        """
        users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in ['id', 'email', 'session_id']:
                raise InvalidRequestError
            users = users.filter_by(**{k: v})
        user = users.first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id, **kwargs) -> None:
        """Updates user's attributes with the passed id.
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k in ["email", "hashed_password", "session_id", "reset_token"]:
                user.k = v

            else:
                raise ValueError
