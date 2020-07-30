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


logger = logging.getLogger('init_quiz_db')


def main():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%b-%d %H:%M:%S (%Z)',
            style='%',
        )
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    quiz_tools_logger = logging.getLogger('quiz_tools')
    quiz_tools_logger.addHandler(console_handler)
    quiz_tools_logger.setLevel(logging.DEBUG)

    redis_tools_logger = logging.getLogger('redis_tools')
    redis_tools_logger.addHandler(console_handler)
    redis_tools_logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Утилита для занесения вопросов викторины в базу данных'
        )
    parser.add_argument('d', help='директория, в которой находятся файлы с вопросами')

    args = parser.parse_args()

    base_dir = dirname(abspath(__file__))
    files_dir = joinpath(base_dir, args.d)
    logger.debug('Files dir: {}'.format(files_dir))

    database = redis_tools.connect_to_redis()

    try:
        question_cards = quiz_tools.get_question_cards(files_dir)
        quiz_tools.add_question_cards_to_database(
                question_cards, 
                database,
            )

    except FileNotFoundError:
        logger.error('Ошибка: Файл не найден', exc_info=True)
    except redis.exceptions.AuthenticationError:
        logger.error('Подключение к базе данных: ошибка аутентификации')



if __name__ == "__main__":
    main()