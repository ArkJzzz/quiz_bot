#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
from os import getenv

from dotenv import load_dotenv


redis_tools_logger = logging.getLogger('redis_tools')
quiz_tools_logger = logging.getLogger('quiz_tools')
bot_tg_logger = logging.getLogger('bot_tg')
bot_vk_logger = logging.getLogger('bot_vk')
init_quiz_db_logger = logging.getLogger('init_quiz_db')

logging.basicConfig(
    format='%(asctime)s %(name)s:%(lineno)d - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
    # level=logging.DEBUG,
)

redis_tools_logger.setLevel(logging.DEBUG)
quiz_tools_logger.setLevel(logging.DEBUG)
bot_tg_logger.setLevel(logging.DEBUG)
bot_vk_logger.setLevel(logging.DEBUG)
init_quiz_db_logger.setLevel(logging.DEBUG)


load_dotenv()
telegram_token = getenv('TELEGRAM_TOKEN')
vk_token = getenv('VK_TOKEN')
redis_host = getenv('REDIS_HOST')
redis_port = getenv('REDIS_PORT')
redis_db_number = getenv('REDIS_DB')
redis_password = getenv('REDIS_PASSWORD')

