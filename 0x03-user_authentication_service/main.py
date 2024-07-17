#!/usr/bin/env python3
""" this script shall query a web server and return the status code """
import requests

URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b410u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ this function shall register a user """
    usr_regis = {
        "email": email,
        "password": password,
        }
    ask = requests.post(f"{URL}/users", data=usr_regis)
    resp = {"email": email, "message": "user created"}
    assert ask.status_code == 200
    ask.json() == resp


def log_in_wrong_password(email: str, password: str) -> None:
    """ this function shall log in with the wrong password """
    usr_log = {
        "email": email,
        "password": password,
        }
    ask = requests.post(f"{URL}/sessions", data=usr_log)
    assert ask.status_code == 401


def profile_unlogged() -> None:
    """ this function shall return a profile when unlogged """
    ask = requests.get(f"{URL}/profile")
    assert ask.status_code == 403


def log_in(email: str, password: str) -> str:
    """ this function shall log in """
    usr_log = {
        "email": email,
        "password": password,
        }
    ask = requests.post(f"{URL}/sessions", data=usr_log)
    respo = {"email": email, "message": "logged in"}
    assert ask.status_code == 200
    assert ask.json() == respo
    return ask.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """ this function shall return a profile when logged """
    cooky = {"session_id": session_id}
    ask = requests.get(f"{URL}/profile", cookies=cooky)
    reqs = requests.get(f"{URL}/profile", cookies=cooky)
    respo = {"email": EMAIL}
    assert ask.status_code == 200
    assert reqs.json() == respo


def log_out(session_id: str) -> None:
    """ this function shall log out """
    cooky = {"session_id": session_id}
    ask = requests.delete(f"{URL}/sessions", cookies=cooky)
    assert ask.status_code == 200


def reset_password_token(email: str) -> str:
    """ this function shall return a reset password token """
    usr_reset = {"email": email}
    ask = requests.post(f"{URL}/reset_password", data=usr_reset)
    tok = ask.json().get("reset_token", None)
    respo = {"email": email, "reset_token": tok}
    assert ask.status_code == 200
    assert ask.json() == respo
    return tok


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ this function shall update the password """
    usr_upd = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
        }
    ask = requests.put(f"{URL}/reset_password", data=usr_upd)
    respo = {"email": email, "message": "Password updated"}
    assert ask.status_code == 200
    assert ask.json() == respo


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
