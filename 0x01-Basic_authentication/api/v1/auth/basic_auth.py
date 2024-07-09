#!/usr/bin/env python3
""" this script shall rep module for API status codes authentication"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ this class shall rep the BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ this method shall extract the base64 authorization header"""
        if authorization_header is None:
            return None
        elif type(authorization_header) is not str:
            return None
        elif authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ this method shall decode the base64 authorization header"""
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) is not str:
            return None
        try:
            base64_authorization_header = base64.b64decode(
                base64_authorization_header)
        except Exception:
            return None
        return base64_authorization_header.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ this method shall extract the user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        elif type(decoded_base64_authorization_header) is not str:
            return None, None
        elif ':' not in decoded_base64_authorization_header:
            return None, None
        log_info = decoded_base64_authorization_header.split(':')
        return log_info[0], log_info[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ this method shall return the user object from credentials"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if user is None or len(user) == 0:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ this method shall return the current user"""
        if request is None:
            return None
        auth_hdr = self.authorization_header(request=request)
        bz64_ath_hd = self.extract_base64_authorization_header(auth_hdr)
        deco_ath_hd = self.decode_base64_authorization_header(bz64_ath_hd)
        get_usr = self.extract_user_credentials(deco_ath_hd)
        usr_obj = self.user_object_from_credentials(user_email=get_usr[0],
                                                    user_pwd=get_usr[1])
        return usr_obj
