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

import redis_tools


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def get_question_cards(files_dir):
    question_cards_from_dir = []
    for root, dirs, files in walkpath(files_dir):
        for filename in files:
            filename = joinpath(root, filename)
            question_cards_from_file = get_question_cards_from_file(filename)
            question_cards_from_dir.extend(question_cards_from_file)
            logger.info('Завершено чтение файла {}'.format(filename))
    
    return question_cards_from_dir


def get_question_cards_from_file(filename):
    ''' Читает файл с вопросами и возвращает список словарей вида:
    {
        'question': 'Текст вопроса',
        'short_answer': 'Ответ' ,
        'long_answer': 'Расширенный ответ, включая комментарий, источник, автора'
    }
    '''
    with open(filename, 'r', encoding='KOI8-R') as my_file:
        questions_data = my_file.read()
    questions_data = questions_data.split('\n\n')

    question_cards_from_file = []
    keys = [
        'question',
        'short_answer',
        'long_answer',
    ]
    question_card = {key: None for key in keys}

    for text_block in questions_data:
        question = re.search(r'^Вопрос \d*:', text_block)
        if question:
            if question_card['question']:
                question_card['long_answer'] = long_answer
                question_cards_from_file.append(question_card)
                question_card = {key: None for key in keys}
            question_card['question'] = clear_text_block(text_block)

        long_answer = ''
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

    return question_cards_from_file


def clear_text_block(text_block):
    '''Удаляет первую строку, лишние переносы строки и пробелы'''

    text_block = text_block.split('\n')[1:]
    text_block = ' '.join(text_block)
    text_block = re.sub(r' {2,}', ' ', text_block)

    return text_block


def add_question_cards_to_database(question_cards, database):
    for question_card in enumerate(question_cards):
        key = 'question_card_{}'.format(question_card[0])
        value = question_card[1]
        redis_tools.set_data_to_database(key, value, database)
    
    logger.debug('Вопросы занесены в базу данных')


def get_random_question_card_number(database):
    pattern = 'question_card_*'
    keys = redis_tools.get_keys_from_database(database, pattern)
    random_number = random.randrange(len(keys))
    question_card_number = keys[random_number]

    return question_card_number


def add_user_to_database(chat_id, source, value, database):
    key = 'user_{source}_{chat_id}'.format(
            source=source, 
            chat_id=chat_id,
        )
    value = {'last_asked_question': value}
    redis_tools.set_data_to_database(key, value, database)

    logger.debug('Пользователь добавлен в базу')


def get_last_asked_question(chat_id, source, database):
    key = 'user_{source}_{chat_id}'.format(
            source=source, 
            chat_id=chat_id,
        )

    user_data = redis_tools.get_value_from_database(key, database)

    return user_data['last_asked_question']


def get_long_answer(question_card_number, database):
    question_card = redis_tools.get_value_from_database(
            key=question_card_number, 
            database=database,
        )

    return question_card['long_answer']


def evaluate_answer(user_answer, chat_id, source, database):
    key = get_last_asked_question(chat_id, source, database)
    question_card = redis_tools.get_value_from_database(key, database)

    exclude_symbols = [',', '.']
    correct_answer = question_card['short_answer'].lower()
    user_answer = user_answer.lower()

    for symbol in exclude_symbols:
        correct_answer = correct_answer.replace(symbol, '')
        user_answer = user_answer.replace(symbol, '')

    logger.debug('\ncorrect_answer: {}\nuser_answer: {}'.format(
            correct_answer, user_answer
        )
    )

    if correct_answer == user_answer:
        return 'Правильный ответ!'
    else: 
        return 'Ответ неправильный, попробуй еще раз.'






if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')





        

