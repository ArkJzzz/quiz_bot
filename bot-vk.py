#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import time
from os import getenv

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from dotenv import load_dotenv

import quiz_tools
import redis_tools


logger = logging.getLogger('bot_vk')

DATABASE = redis_tools.connect_to_redis()


def handle_new_question(event, vk, keyboard):
    chat_id = event.user_id
    question_card_number = quiz_tools.get_random_question_card_number(DATABASE)
    quiz_tools.add_userdata_to_database(
        chat_id=chat_id,
        source='vk',
        question_card_number=question_card_number,
        database=DATABASE,
    )
    question = quiz_tools.get_question(question_card_number, DATABASE)
    logger.debug(
        'user: {}\tquestion_card_number: {}'.format(
            chat_id,
            question_card_number,
        )
    )

    vk.messages.send(
        peer_id = chat_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=question, 
    )

def handle_capitulate(event, vk, keyboard):
    chat_id = event.user_id
    question_card_number = quiz_tools.get_last_asked_question(
            chat_id=chat_id,
            source='vk',
            database=DATABASE,
        )
    answer = quiz_tools.get_long_answer(question_card_number, DATABASE)
    vk.messages.send(
        peer_id = chat_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=answer, 
    )

def handle_answer_attempt(event, vk, keyboard):
    chat_id = event.user_id
    user_answer = event.text
    verdict = quiz_tools.evaluate_answer(
            user_answer=user_answer, 
            chat_id=chat_id, 
            source='vk', 
            database=DATABASE,
        )
    vk.messages.send(
        peer_id = chat_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=verdict,
    )


def send_text_message(event, vk, keyboard):
    vk.messages.send(
        peer_id = event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Привет, это бот для викторин!\nНажми "Новый вопрос", чтобы начать.',
    )
    

def main():
    # init
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

    load_dotenv()
    vk_token = getenv('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token) 
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Сдаться', color=VkKeyboardColor.DEFAULT)

    # do
    try:
        logger.debug('Стартуем бота')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Привет':
                    send_text_message(event, vk, keyboard)
                elif event.text == 'Новый вопрос':
                    handle_new_question(event, vk, keyboard)
                elif event.text == 'Сдаться':
                    handle_capitulate(event, vk, keyboard)
                else:
                    handle_answer_attempt(event, vk, keyboard)
    except KeyboardInterrupt:
        logger.info('Бот остановлен')
    except ConnectionError:
        logger.error('Connection aborted')
    except requests.exceptions.ReadTimeout:
        logger.error('Переподключение к серверам ВК')
        time.sleep(3)
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)
            

if __name__ == "__main__":
    main()