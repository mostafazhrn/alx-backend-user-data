#!/usr/bin/env python3
""" this script shall encrypt a string using bcrypt """
import bcrypt
from db import DB
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str = '') -> str:
    """ this function shall hash a password """
    hsh_passwd = bcrypt.hashpw(password.encode('utf-8'),
                               bcrypt.gensalt(prefix=b"2b"))
    str_hsh: str = str(hsh_passwd.decode())
    return str_hsh


def _generate_uuid() -> str:
    """ this function shall generate a uuid """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ This instance shall take email paswwd return user registered"""
        try:
            consuil = self._db.find_user_by(email=email)
            raise ValueError(f'<{consuil.email}> already exists')
        except NoResultFound:
            pswd: str = _hash_password(password)
            usr = self._db.add_user(email, pswd)
        return usr

    def valid_login(self, email: str, password: str) -> bool:
        """ this instance shall validate login"""
        if email is None or password is None:
            return False
        try:
            usr: User = self._db.find_user_by(email=email)
            passwd: bytes = str.encode(usr.hashed_password)
            valid: bool = bcrypt.checkpw(password.encode('utf-8'), passwd)
            return valid
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ this instance shall create a session"""
        try:
            usr = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(usr.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """ this instance shall get user from session id"""
        if session_id is None:
            return None
        try:
            usr = self._db.find_user_by(session_id=session_id)
            return usr
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: str) -> None:
        """ this instance shall destroy session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ this instance shall get reset password token"""
        if email is None:
            raise

        try:
            usr = self._db.find_user_by(email=email)
            token: str = _generate_uuid()
            self._db.update_user(usr.id, reset_token=token)
            return token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ this instance shall update password"""
        if reset_token is None or password is None:
            return None
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        nuevo_passwd = _hash_password(password)
        self._db.update_user(usr.id,
                             hashed_password=nuevo_passwd, reset_token=None)
        return None
