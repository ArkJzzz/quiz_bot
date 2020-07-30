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


logger = logging.getLogger('quiz_bot.redis_tools')


def connect_to_redis():
    database = redis.Redis(
        host=settings.redis_host, 
        port=settings.redis_port, 
        db=settings.redis_db_number, 
        password=settings.redis_password,
    )
    logger.debug('Подключение к redis установлено')

    return database


def clear_database(database):
    keys = database.keys()
    for key in keys:
        database.delete(key)
        logger.info('БД: удалена запись: {}'.format(key))


if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')





        

