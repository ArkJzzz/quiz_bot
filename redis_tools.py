#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import re
import json
import random
from os import getenv
from os import walk as walkpath
from os.path import join as joinpath

import redis
from dotenv import load_dotenv

import settings


logger = logging.getLogger('redis_tools')


def connect_to_redis():
    database = redis.Redis(
        host=settings.redis_host, 
        port=settings.redis_port, 
        db=settings.redis_db_number, 
        password=settings.redis_password,
    )

    return database


def add_card_to_database(question_card, database):
    value = json.dumps(question_card)
    database.rpush('question_cards', value)
    logger.info('БД: добавлена запись: {}'.format(question_card))


def get_keys_from_database(database, pattern='*'):
    keys = database.keys(pattern=pattern)
    decoded_keys = []
    for key in keys:
        decoded_key = key.decode('utf-8')
        decoded_keys.append(decoded_key)

    return decoded_keys


def get_value_from_database(key, database):
    logger.debug(key)
    value = database.get(key)
    value = json.loads(value)

    return value


def clear_database(database):
    keys = database.keys()
    for key in keys:
        database.delete(key)
        logger.info('БД: удалена запись: {}'.format(key))


if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')





        

