#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging

import redis
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import settings
import quiz_tools
import redis_tools


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

DATABASE = redis_tools.connect_to_redis()


def handle_new_question(event, vk, keyboard):
    question_card_number = quiz_tools.get_random_question_card_number(DATABASE)
    question_card = redis_tools.get_value_from_database(
            key=question_card_number, 
            database=DATABASE,
        )
    chat_id = event.user_id
    quiz_tools.add_user_to_database(
            chat_id=chat_id,
            source='vk',
            value=question_card_number,
            database=DATABASE,
        )
    logger.debug(
        'user: {}\nquestion_card_number: {}\n{}'.format(
            chat_id,
            question_card_number,
            question_card,
        )
    )
    question = question_card['question']

    vk.messages.send(
        peer_id = chat_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=question, 
    )

def handle_capitulate(event, vk, keyboard):
    chat_id = event.user_id
    last_asked_question = quiz_tools.get_last_asked_question(
        chat_id=chat_id, 
        source='vk', 
        database=DATABASE,
        )
    answer = quiz_tools.get_long_answer(last_asked_question, DATABASE)
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
    vk_session = vk_api.VkApi(token=settings.vk_token) 
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
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)
            

if __name__ == "__main__":
    main()