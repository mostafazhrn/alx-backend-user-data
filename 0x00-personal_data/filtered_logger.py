#!/usr/bin/env python3
""" This script shall obfuscate certain fields in a log message"""
import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = '***'
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ';'

    def __init__(self, fields: List[str]):
        """ this shall rep constructor  method"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ This shall rep the format method"""
        res = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields, self.REDACTION, res, self.SEPARATOR)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ this instance shall return a database connection"""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """ This function shall obfuscate certain fields in a log message"""
    for field in fields:
        message = re.sub(rf"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """ this instance shall return logger with streamhandler red formatter"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    aim_hnadler = logging.StreamHandler()
    aim_hnadler.setLevel(logging.INFO)
    formatte = RedactingFormatter(list(PII_FIELDS))
    logger.addHandler(aim_hnadler)
    return logger
