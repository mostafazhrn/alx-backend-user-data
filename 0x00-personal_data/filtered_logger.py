#!/usr/bin/env python3
""" This script shall obfuscate certain fields in a log message"""
import re
from typing import List
import logging
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


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """ This function shall obfuscate certain fields in a log message"""
    for field in fields:
        message = re.sub(rf"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message
