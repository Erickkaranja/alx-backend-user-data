#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

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

    def add_user(self, email: str, hashed_password: str) -> User:
        """creating a user object.
        """
        new_user: User = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """finding user by passed key.
        """
        users = self._session.query(User)
        for k, v in kwargs.items():
            users = users.filter_by(**{k: v})
        user = users.first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id, **kwargs):
        """Updates user's attributes
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k in ["email", "hashed_password", "session_id", "reset_token"]:
                user.k = v

            else:
                raise ValueError
