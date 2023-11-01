#!/usr/bin/python3
import re

def filter_datum(fields, redaction, message, separator=';'):
    # Split the message into individual fields based on the separator
    parts = message.split(separator)

    # Obfuscate the specified fields
    for field in fields:
        pattern = re.compile(rf'{field}=[^;]+')
        message = pattern.sub(f'{field}={redaction}', message)

    return message

# Example usage:
fields_to_obfuscate = ['password', 'date_of_birth']
redaction_character = 'xxx'
log_message = "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=1990-01-01"
separator_character = ';'

obfuscated_log = filter_datum(fields_to_obfuscate, redaction_character, log_message, separator_character)
print(obfuscated_log)
