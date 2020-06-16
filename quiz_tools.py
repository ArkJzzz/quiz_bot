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
    with open(filename, 'r', encoding='KOI8-R') as my_file:
        questions_data = my_file.read()
    questions_data = questions_data.split('\n\n')

    question_cards = []
    keys = [
        'question',
        'short_answer',
        'long_answer', # Включая Комментарий, Источник, Автор
    ]
    question_card = {key: None for key in keys}

    for text_block in questions_data:
        question = re.search(r'^Вопрос \d*:', text_block)
        if question:
            if question_card['question']:
                question_card['long_answer'] = long_answer
                question_cards.append(question_card)
                question_card = {key: None for key in keys}
            question_card['question'] = clear_text_block(text_block)

        short_answer = re.search(r'^Ответ:', text_block)
        if short_answer:
            short_answer = clear_text_block(text_block)
            short_answer = re.sub(r'[\[\]\(\)]' , '', short_answer)
            question_card['short_answer'] = short_answer
            long_answer = 'Ответ:\n{}\n\n'.format(short_answer)

        comment = re.search(r'^Комментарий:', text_block)
        if comment:
            comment = clear_text_block(text_block)
            long_answer += 'Комментарий:\n{}\n\n'.format(comment)

        source = re.search(r'^Источник:', text_block)
        if source:
            source = clear_text_block(text_block)
            long_answer += 'Источник:\n{}\n\n'.format(source)
        
        author = re.search(r'^Автор:', text_block)
        if author:
            author = clear_text_block(text_block)
            long_answer += 'Автор:\n{}'.format(author)

    return question_cards


def clear_text_block(text_block):
    '''Удаляет первую строку, лишние переносы строки и пробелы'''
    
    text_block = text_block.split('\n')[1:]
    text_block = ' '.join(text_block)
    text_block = re.sub(r' {2,}', ' ', text_block)

    return text_block


def get_random_key(database):
    keys = database.keys(pattern='question_card_')
    random_number = random.randrange(len(keys))
    random_key = keys[random_number].decode('utf-8')

    return random_key


def get_dict_value(key, database):
    value = database.get(key)
    value = json.loads(value)

    return value




if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')





        

