#!/usr/bin/env python3
""" This script shall hash a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ This function shall hash a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
