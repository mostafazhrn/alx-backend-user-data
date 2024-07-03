#!/usr/bin/env python3
""" This script shall obfuscate certain fields in a log message"""
import re
from typing import List
import logging
import os


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """ This function shall obfuscate certain fields in a log message"""
    for field in fields:
        message = re.sub(rf"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message
