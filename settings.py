#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
from os import getenv

from dotenv import load_dotenv


logger = logging.getLogger('quiz_bot')


logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
        fmt='%(asctime)s %(name)s:%(lineno)d - %(message)s',
        datefmt='%Y-%b-%d %H:%M:%S (%Z)',
        style='%',
    )
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)



load_dotenv()
telegram_token = getenv('TELEGRAM_TOKEN')
vk_token = getenv('VK_TOKEN')
redis_host = getenv('REDIS_HOST')
redis_port = getenv('REDIS_PORT')
redis_db_number = getenv('REDIS_DB')
redis_password = getenv('REDIS_PASSWORD')

