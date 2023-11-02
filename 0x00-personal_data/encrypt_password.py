#!/usr/bin/env python3
'''implementing an encryption module using bcrypt.'''
import bcrypt


def hash_password(password: str) -> str:
    '''implementing password hashing using bcrypt'''
    bytes: byte = password.encode('utf-8')
    salt: str = bcrypt.gensalt()
    hash: byte = bcrypt.hashpw(bytes, salt)
    return hash


def is_valid(hashed_password: byte, password: str) -> bool:
    '''checks a password against a hashed value.'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
