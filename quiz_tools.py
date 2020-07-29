#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import re
import json
import random

from os import getenv
from os import walk as walkpath
from os.path import join as joinpath

import redis
from dotenv import load_dotenv


logger = logging.getLogger('quiz_tools')


def get_question_cards(files_dir):
    question_cards_from_dir = []
    for root, dirs, files in walkpath(files_dir):
        for filename in files:
            filename = joinpath(root, filename)
            questions_data = read_file(filename)
            question_cards_from_file = get_question_cards_from_data(
                                        questions_data
                                    )
            question_cards_from_dir.extend(question_cards_from_file)
            logger.info('Завершено чтение файла {}'.format(filename))
    
    return question_cards_from_dir


def read_file(filename):
    with open(filename, 'r', encoding='KOI8-R') as my_file:
        questions_data = my_file.read()
    questions_data = questions_data.split('\n\n')

    return questions_data


def get_question_cards_from_data(questions_data):
    ''' возвращает список вопросных карточек, каждая карточка вида:
    [questoin, short_answer, long_answer]
    '''
    question_cards_from_file = []
    question_card = [None for i in range(3)]

    for text_block in questions_data:
        question = re.search(r'^Вопрос \d*:', text_block)
        if question:
            if question_card and question_card[0]:
                question_card[2] = long_answer
                question_cards_from_file.append(question_card)
                logger.debug(question_card)
                question_card = [None for i in range(3)]
            question_card[0] = clear_text_block(text_block)

        short_answer = re.search(r'^Ответ:', text_block)
        if short_answer:
            short_answer = clear_text_block(text_block)
            short_answer = re.sub(r'[\[\]\(\)]' , '', short_answer)
            question_card[1] = short_answer
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
    for question_card in question_cards:
        add_question_card_to_database(question_card, database)
    
    logger.debug('Вопросы занесены в базу данных')


def add_question_card_to_database(question_card, database):
    value = json.dumps(question_card)
    database.rpush('question_cards', value)
    logger.info('В БД добавлена запись: {}'.format(question_card))


def get_random_question_card_number(database):
    num_of_question_cards = database.llen('question_cards')
    logger.debug('Всего карточек в базе: {}'.format(num_of_question_cards))
    random_number = random.randrange(num_of_question_cards)
    logger.debug('random_number: {}'.format(random_number))

    question_card = database.lindex('question_cards', random_number)

    logger.debug('Выбрана карточка: : {}'.format(
            json.loads(question_card)
        )
    )

    return random_number


def add_userdata_to_database(chat_id, source, question_card_number, database):
    hash_name = '{source}_users'.format(source=source)
    database.hset(hash_name, chat_id, question_card_number)

    logger.info('В БД добавлена запись о пользователе: {}: {}'.format(
                        hash_name,
                        chat_id,
                    )
                )


def get_last_asked_question(chat_id, source, database):
    hash_name = '{source}_users'.format(source=source)
    last_asked_question = database.hget(hash_name, chat_id)
    logger.debug('last_asked_question: {}'.format(last_asked_question.decode()))

    return last_asked_question.decode()


def get_question(question_card_number, database):
    question_card = database.lindex('question_cards', question_card_number)
    question_card = json.loads(question_card)

    logger.debug('question: {}'.format(question_card[0]))

    return question_card[0]


def get_correct_answer(chat_id, source, database):
    question_card_number = get_last_asked_question(chat_id, source, database)
    question_card = database.lindex('question_cards', question_card_number)
    question_card = json.loads(question_card)
    correct_answer = question_card[1].lower()

    logger.debug('short answer: {}'.format(question_card[1]))

    return correct_answer


def get_long_answer(question_card_number, database):
    question_card = database.lindex('question_cards', question_card_number)
    question_card = json.loads(question_card)

    logger.debug('long answer: {}'.format(question_card[2]))

    return question_card[2]


def clear_answer(answer):
    exclude_symbols = [',', '.', '\"']
    for symbol in exclude_symbols:
        answer = answer.replace(symbol, '')
    return answer


def evaluate_answer(user_answer, chat_id, source, database):
    correct_answer = get_correct_answer(chat_id, source, database)
    correct_answer = clear_answer(correct_answer)
    user_answer = user_answer.lower()
    user_answer = clear_answer(user_answer)

    logger.debug('evaluate_answer:\ncorrect_answer: {}\nuser_answer: {}'.format(
            correct_answer, 
            user_answer,
        )
    )

    if correct_answer == user_answer:
        return 'Правильный ответ!'
    else: 
        return 'Ответ неправильный, попробуй еще раз.'


if __name__ == "__main__":
    print('Эта утилита не предназначена для запуска напрямую')