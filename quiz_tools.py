#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import re
import json
import random

from os import getenv
from os import walk as walkpath
from os.path import join as joinpath

from dotenv import load_dotenv


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def add_question_cards_to_database(files_dir, database):
    question_cards = get_question_cards(files_dir)
    for question_card in enumerate(question_cards):
        key = 'question_card_{}'.format(question_card[0])
        value = json.dumps(question_card[1])
        database.set(key, value)
        logger.debug('Вопрос {} занесен в базу данных'.format(key))


def get_question_cards(files_dir):
    question_cards = []
    for root, dirs, files in walkpath(files_dir):
        for filename in files:
            filename = joinpath(root, filename)
            question_cards = get_question_cards_from_file(filename)
            question_cards.extend(question_cards)
            logger.info('Завершено чтение файла {}'.format(filename))
    
    return question_cards


def get_question_cards_from_file(filename):
    question_cards = []
    keys = [
        'Вопрос',
        'Ответ',
        'Комментарий',
        'Источник',
        'Автор',
    ]
    question_card = {key: None for key in keys}

    with open(filename, 'r', encoding='KOI8-R') as my_file:
        question_data = my_file.read()

    question_data = question_data.split('\n\n')

    for string in question_data:
        if string[:6] == 'Вопрос' and question_card['Вопрос']:
            question_cards.append(question_card)
            question_card = {key: None for key in keys}
        
        string_chunks = string.split('\n')
        key = re.findall(r'^\w+', string_chunks[0])
        value = ' '.join(string_chunks[1:])

        if key:
            if key[0] in keys:
                if key[0] == 'Ответ':
                    value = re.sub(r'[\.\[\]]', '', value)
                question_card[key[0]] = value

    return question_cards


def get_random_key(pattern, database):
    keys = database.keys(pattern=pattern)
    random_number = random.randrange(len(keys))
    random_key = keys[random_number].decode('utf-8')

    return random_key


def get_dict_value(key, database):
    value = database.get(key)
    value = json.loads(value)

    return value


def add_user_to_database(key, value, database):
    value = {"last_asked_question": value}
    logger.debug('БД: добавлена запись: {}: {}'.format(key, value))
    value = json.dumps(value)
    database.set(key, value)




if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')





        

