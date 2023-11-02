#!/usr/bin/env python3
'''implementing a filter_logger module.'''
import os
import re
from typing import List, Tuple, Dict
import logging
import mysql.connector

def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    for field in fields:
        message = re.sub('{}=[^{}]+'.format(field, separator),
                         '{}={}'.format(field, redaction), message)
    return message



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: str = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg: str = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)

PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    '''creates a logging.Logger object.'''
    logger = login.getlogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger

def get_db():
    ''''''
    config: Dict = {
        'user': os.getenv("PERSONAL_DATA_DB_USERNAME", 'root'),
        'password': os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        'host': os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        'database': os.getenv("PERSONAL_DATA_DB_NAME"),
    }

    return mysql.connector.connect(**config)
