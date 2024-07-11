#!/usr/bin/env python3
""" this script shall rep module for API status codes authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, List, Dict
import uuid
from uuid import UUID, uuid4


class SessionAuth(Auth):
    """ this class shall rep the SessionAuth class"""
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ this method shall create a session"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ This instance shall return USER id"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ this instance shall return user instance based on the cookie"""
        session_id = self.session_cookie(request)
        user_id: str = self.user_id_for_session_id(session_id)
        user: TypeVar('User') = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ this instance shall destroy the session"""
        if request is None:
            return False
        session_id: str = self.session_cookie(request)
        if session_id is None:
            return False
        user_id: str = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass
        return True
