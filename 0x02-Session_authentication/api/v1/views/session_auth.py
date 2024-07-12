#!/usr/bin/env python3
""" this Module shall rep an API status codes of the SessionAuth class"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.user import User
from os import getenv
from typing import TypeVar, List
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ This instance shall login the user """
    email = request.form.get('email')
    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)
    password = request.form.get('password')

    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    user_found = User.search({'email': email})
    if len(user_found) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for usr in user_found:
        if usr.is_valid_password(password):
            session_id = auth.create_session(usr.id)
            SESSION_NAME = getenv('SESSION_NAME')
            respo = make_response(usr.to_json())
            respo.set_cookie(SESSION_NAME, session_id)
            return respo

    return make_response(jsonify({"error": "wrong password"}), 401)


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ This instance shall logout the user """
    desto = auth.destroy_session(request)
    if desto is False:
        abort(404)
    return jsonify({}), 200
