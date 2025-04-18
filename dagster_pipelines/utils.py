from __future__ import annotations
from typing import TYPE_CHECKING
import logging
import sys
import json
import boto3
from botocore.exceptions import ClientError

if TYPE_CHECKING:
    import uuid

def get_secret(secret_name, region_name) -> dict:

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return json.loads(secret)

if TYPE_CHECKING:
    import uuid

def make_guid(*args) -> uuid.UUID:
    '''Returns a reproducible guid based on the values passed'''
    import hashlib
    import uuid

    concat_str = ''.join(map(str, args))
    hash_val = hashlib.sha1(concat_str.encode()).hexdigest()
    return uuid.UUID(hash_val[:32])

def get_console_handler() -> logging.StreamHandler:
   FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_logger(logger_name: str) -> logging.Logger:
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.INFO)
   logger.addHandler(get_console_handler())
   logger.propagate = False
   return logger
