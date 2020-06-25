#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
from os import getenv
from os.path import dirname
from os.path import abspath
from os.path import join as joinpath

from dotenv import load_dotenv


logging.basicConfig(
    format='%(asctime)s %(name)s - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

load_dotenv()

BASE_DIR = dirname(abspath(__file__))
QUIZ_QUESTION_DIR = 'test/'
quiz_question_dir = joinpath(BASE_DIR, QUIZ_QUESTION_DIR)

telegram_token = getenv('TELEGRAM_TOKEN')
vk_token = getenv('VK_TOKEN')

redis_host = getenv('REDIS_HOST')
redis_port = getenv('REDIS_PORT')
redis_db_number = 0
redis_password = getenv('REDIS_PASSWORD')

