#!/usr/bin/env python3
""" this script shall rep module for API status codes authentication"""
from models.base import Base


class UserSession(Base):
    """ this class shall represent the user class session"""
    def __init__(self, *args: list, **kwargs: dict):
        """ this method shall initialize the UserSession class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.session_id = kwargs.get('session_id', "")
