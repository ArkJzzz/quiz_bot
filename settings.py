#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
from os import getenv
from os.path import dirname
from os.path import abspath
from os.path import join as joinpath

from dotenv import load_dotenv


logging.basicConfig(
    format='%(asctime)s %(name)s:%(lineno)d - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

load_dotenv()

telegram_token = getenv('TELEGRAM_TOKEN')

vk_token = getenv('VK_TOKEN')

redis_host = getenv('REDIS_HOST')
redis_port = getenv('REDIS_PORT')
redis_db_number = getenv('REDIS_DB')
redis_password = getenv('REDIS_PASSWORD')

