#!/usr/bin/env python3
""" this script shall rep module for API status codes authentication"""
from api.v1.auth.session_auth import SessionAuth
from typing import TypeVar, List, Dict
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ this class shall rep the SessionExpAuth class"""
    session_duration: int = 0

    def __init__(self):
        """ this method shall initialize the SessionExpAuth class"""
        SESSION_DURATION = getenv('SESSION_DURATION', 0)
        try:
            SESSION_DURATION = int(SESSION_DURATION)
        except Exception:
            SESSION_DURATION = 0

        self.session_duration = SESSION_DURATION

    def create_session(self, user_id=None):
        """ this method shall create a session"""
        sesh_id = super().create_session(user_id)
        if sesh_id is None:
            return None
        sesh_dict: Dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[sesh_id] = sesh_dict
        return sesh_id

    def user_id_for_session_id(self, session_id=None):
        """ this instance shall return USER id"""
        if session_id is None or\
           session_id not in self.user_id_by_session_id.keys():
            return None
        sesh_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0 or sesh_dict is None:
            return sesh_dict.get('user_id', None)
        created_at = sesh_dict.get('created_at', None)
        if created_at is None:
            return None
        expi_sesh = created_at + timedelta(seconds=self.session_duration)
        if expi_sesh < datetime.now():
            return None
        return sesh_dict.get('user_id', None)
