#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import argparse
from os.path import dirname
from os.path import abspath
from os.path import join as joinpath

import redis

import quiz_tools
import redis_tools


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def main():

    parser = argparse.ArgumentParser(
        description='Утилита для занесения вопросов викторины в базу данных'
        )
    parser.add_argument('d', help='директория, в которой находятся файлы с вопросами')

    args = parser.parse_args()

    BASE_DIR = dirname(abspath(__file__))
    files_dir = joinpath(BASE_DIR, args.d)
    logger.debug('Files dir: {}'.format(files_dir))

    DATABASE = redis_tools.connect_to_redis()

    try:
        question_cards = quiz_tools.get_question_cards(files_dir)
        quiz_tools.add_question_cards_to_database(
                question_cards, 
                DATABASE,
            )

    except FileNotFoundError:
        logger.error('Ошибка: Файл не найден', exc_info=True)
    except redis.exceptions.AuthenticationError:
        logger.error('Подключение к базе данных: ошибка аутентификации')



if __name__ == "__main__":
    main()