#!/usr/bin/env python3
'''implementing an encryption module using bcrypt.'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''implementing password hashing using bcrypt'''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checks a password against a hashed value.'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
