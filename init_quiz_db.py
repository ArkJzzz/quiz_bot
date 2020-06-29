#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging

import redis

import settings
import quiz_tools
import redis_tools


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def main():

    DATABASE = redis.Redis(
        host=settings.redis_host, 
        port=settings.redis_port, 
        db=settings.redis_db_number, 
        password=settings.redis_password,
    )

    files_dir = settings.quiz_question_dir
    logger.debug('Files dir: {}'.format(files_dir))


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