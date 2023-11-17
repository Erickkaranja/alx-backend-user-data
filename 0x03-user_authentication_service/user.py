#!/usr/bin/env python3
"""creating a sqlalchemy model user."""

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """initializing class user."""
    __tablename__: str = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250))
    reset_token: str = Column(String(250))
