#!usr/bin/python3

__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import os
import logging
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import settings
import quiz_tools
import redis_tools


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def send_text_message(event, vk, keyboard):

    vk.messages.send(
        peer_id = event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=event.text,
        
    )
    

def main():
    # init
    vk_session = vk_api.VkApi(token=settings.vk_token) 
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    logger.debug('все готово')

    # do

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Сдаться', color=VkKeyboardColor.DEFAULT)


    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                logger.debug('Новое сообщение:')
                logger.debug('Для меня от: {}'.format(event.user_id))
                logger.debug('Текст:{}'.format(event.text))
                send_text_message(event, vk, keyboard)
    except KeyboardInterrupt:
        logger.info('Бот остановлен')
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)
            

if __name__ == "__main__":
    main()