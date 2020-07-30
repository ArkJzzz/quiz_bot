#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
from os import getenv

import redis
from dotenv import load_dotenv


logger = logging.getLogger('redis_tools')


def connect_to_redis():
    load_dotenv()
    database = redis.Redis(
        host=getenv('REDIS_HOST'), 
        port=getenv('REDIS_PORT'), 
        db=getenv('REDIS_DB'), 
        password=getenv('REDIS_PASSWORD'),
    )
    logger.info('Подключение к redis установлено')

    return database


def clear_database(database):
    keys = database.keys()
    for key in keys:
        database.delete(key)
        logger.info('БД: удалена запись: {}'.format(key))


if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')





        

