#!/usr/bin/env python3
'''implementing a filter_logger module.'''

import os
import re
from typing import List, Tuple, Dict
import logging
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''implementing a filter function.
       Args:
           fields: input fields whose data is to be obfuscated.
           redaction: sting to obfuscate.
           message: contains field to be obfuscated.
       Return:
           a message with obfuscated fields.
    '''
    for field in fields:
        message: str = re.sub('{}=[^{}]+'.format(field, separator),
                              '{}={}'.format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, *args, **kwargs):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = list(args)

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum.
        """
        record.msg: str = filter_datum(self.fields, self.REDACTION,
                                       record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    '''creates a logging.Logger object.'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db():
    '''creating a connector object to our mysql data.'''
    config: Dict = {
        'user': os.getenv("PERSONAL_DATA_DB_USERNAME", 'root'),
        'password': os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        'host': os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        'database': os.getenv("PERSONAL_DATA_DB_NAME"),
    }

    return mysql.connector.connect(**config)


def main() -> None:
    '''main function that retrieves all objects from users table an redact PII.
    '''
    log: logging.Logger = get_logger()
    db: mysql.connector = get_db()
    cursor: cursor.MySQLCursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    message: str = 'name={}; email={}; phone={}; '
    message += 'ssn={}; password={}; ip={}; last_login={}; user_agent={};'
    for row in cursor.fetchall():
        log.info(message.format(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6], row[7]))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
