#!/usr/bin/env python3
""" this script shall set up a basic flask app """
from flask import Flask, jsonify, request, abort, make_response, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/reset_password', methods=['PUT'])
def reset_password() -> str:
    """ this instance shall reset a password """
    try:
        email = request.form['email']
        toke_rest = request.form['reset_token']
        nuevo_pswd = request.form['new_password']
    except KeyError:
        abort(403)
    try:
        AUTH.update_password(toke_rest, nuevo_pswd)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updates"}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """ this instance shall get a reset password token """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)
    toke: str = ''
    try:
        toke = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": toke}), 200


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """ this instance shall init the log out """
    sesh_id = request.cookies.get('session_id', None)
    if sesh_id is None:
        abort(403)
    usr = AUTH.get_user_from_session_id(sesh_id)
    if usr is None:
        abort(403)
    AUTH.destroy_session(usr.id)
    return redirect('/', code=302)


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    """ this instance shall init the log in """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(401)
    if (AUTH.valid_login(email, password)):
        sesh_id = AUTH.create_session(email)
        if sesh_id is not None:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', sesh_id)
            return response
    abort(401)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ this instance shall return a profile """
    sesh_id = request.cookies.get('session_id', None)
    if sesh_id is None:
        abort(403)
    usr = AUTH.get_user_from_session_id(sesh_id)
    if usr is None:
        abort(403)
    return jsonify({"email": usr.email}), 200


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """ this instance shall return a greeting """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """ this instance shall register a user """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        usr = AUTH.register_user(email, password)
    except ValueError:
        msgs = {"message": "email already registered"}
        return jsonify(msgs), 400
    msgs = {"email": usr.email, "message": "user created"}
    return jsonify(msgs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
