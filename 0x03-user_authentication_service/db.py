#!/usr/bin/env python3
"""This script shall rep the DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ this instance shall make user"""
        nuevo_usr = User(email=email, hashed_password=hashed_password)
        self._session.add(nuevo_usr)
        self._session.commit()
        return nuevo_usr

    def find_user_by(self, **kwargs) -> User:
        """ this instance shall find user"""
        if not kwargs:
            raise InvalidRequestError
        cle_col = User.__table__.columns.keys()
        for cle in kwargs.keys():
            if cle not in cle_col:
                raise InvalidRequestError
        usrs = self._session.query(User).filter_by(**kwargs).first()
        if usrs is None:
            raise NoResultFound
        return usrs

    def update_user(self, user_id: int, **kwargs) -> None:
        """ this instance shall update user"""
        if not kwargs:
            return None
        usr = self.find_user_by(id=user_id)
        cle_col = User.__table__.columns.keys()
        for cle in kwargs.keys():
            if cle not in cle_col:
                raise ValueError
        for cle, val in kwargs.items():
            setattr(usr, cle, val)
        self._session.commit()
