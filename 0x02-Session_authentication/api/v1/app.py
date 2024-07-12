#!/usr/bin/env python3
""" Module for API status codes """
from flask import Flask, jsonify, request, abort
from os import getenv
from api.v1.views import app_views
from flask_cors import (CORS, cross_origin)
import os
from typing import List, TypeVar


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ This instance shall handle all error 404 responses """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ This instance shall handle unauthorized error handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ This instance shall handle forbidden error handler """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """ This instance shall handle all before request auth"""
    if auth is None:
        return
    ex_pth = ['/api/v1/status/', '/api/v1/unauthorized/',
              '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    if not auth.require_auth(request.path, ex_pth):
        return

    if (auth.authorization_header(request)) is None\
       and (auth.session_cookie(request)) is None:
        abort(401)

    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)
    request.current_user = current_user


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", 5000)
    app.run(host=host, port=port)
