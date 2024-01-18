#!/usr/bin/env python3
"""impleenting basic authentication."""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """initializing class BasicAuth."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """implementing a base64 authorization key."""
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        base64_credentials = authorization_header[len('Basic '):]

        return base64_credentials

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """returns the decoded value of a Base64 string."""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        return decoded_bytes.decode('utf-8', errors='replace')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """that returns the user email and password
           from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password =\
            decoded_base64_authorization_header.split(':', 1)

        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """obtains user object from passed user credential user_mail and
           user_pwd
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})[0]
            if user.is_valid_password(user_pwd):
                return user
        except IndexError:
            return None
        except AttributeError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current users based on the passed credentials."""
        auth_header: str = self.authorization_header(request)
        base64cred: str = self.extract_base64_authorization_header(auth_header)
        str_creds: str = self.decode_base64_authorization_header(base64cred)
        credentials: str = self.extract_user_credentials(str_creds)
        if credentials is None or len(credentials) != 2:
            return None
        user: str = self.user_object_from_credentials(credentials[0],
                                                      credentials[1])
        return user
