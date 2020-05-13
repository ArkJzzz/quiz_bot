#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import re

from os import walk as walkpath
from os.path import join as joinpath


logger = logging.getLogger(__file__)
logging.basicConfig(
    format='%(asctime)s %(name)s - %(message)s', 
    datefmt='%Y-%b-%d %H:%M:%S (%Z)',
)
logger.setLevel(logging.DEBUG)


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
        'Зачет',
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
                if key[0] in ['Ответ', 'Зачет']:
                    value = re.sub(r'[\.\[\]]', '', value)
                question_card[key[0]] = value

    return question_cards


if __name__ == "__main__":
	print('Эта утилита не предназначена для запуска напрямую')