#!/usr/bin/env python3
""" this script shall rep module for API status codes authentication"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ this class shall rep the SessionDBAuth class"""
    def create_session(self, user_id=None):
        """ this method shall create a session"""
        sesh_id = super().create_session(user_id)
        if sesh_id is None:
            return None
        new_sesh = UserSession(
            user_id=user_id, session_id=sesh_id)

        if new_sesh is None:
            return None
        new_sesh.save()
        UserSession.save_to_file()
        return sesh_id

    def user_id_for_session_id(self, session_id=None):
        """ this instance shall return USER id"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        sesh = UserSession.search({'session_id': session_id})
        if len(sesh) == 0:
            return None
        usr = sesh[0]
        if usr is None:
            return None
        exp_session = usr.created_at + \
            timedelta(seconds=self.session_duration)

        if exp_session < datetime.now():
            return None
        return usr.user_id

    def destroy_session(self, request=None):
        """ this instance shall destroy the session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()
        sesh = UserSession.search({'session_id': session_id})
        if len(sesh) == 0:
            return False
        usr = sesh[0]
        if usr is None:
            return False
        try:
            usr.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
