#!/usr/bin/env python3
'''implementing a filter_logger module.'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: List[str],
                 separator: str) -> str:
    parts = message.split(separator)
    for field in fields:
        pattern = re.compile(rf'{field}=[^;]+')
        message = pattern.sub(f'{field}={redaction}', message)
    return message
