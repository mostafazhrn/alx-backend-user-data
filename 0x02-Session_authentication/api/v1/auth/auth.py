#!/usr/bin/env python3
""" this script shall rep module for API status codes """
from flask import Flask, jsonify, request, abort
from typing import List, TypeVar
from os import getenv


class Auth:
    """ this class shall rep the Auth class"""

    def __init__(self):
        """ this method shall initialize the Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ this method shall require authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for pths in excluded_paths:
            if pths.endswith('*'):
                if path.startswith(pths[:-1]):
                    return False
            elif path == pths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ this method shall return the authorization header"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ this method shall return the current user"""
        return None

    def session_cookie(self, request=None):
        """ this method shall return the session cookie"""
        if request is None:
            return None
        sesh_envo = getenv('SESSION_NAME', None)
        cookies_sesh = request.cookies.get(sesh_envo, None)

        return cookies_sesh
