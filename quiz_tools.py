#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

#####################################################################
# TODO 
#
# Переделать quiz-tools: 
#	возвратить один словарь из всех вопросов из всех файлов
# Вынести quiz-tools в отдельный файл
# Выбор случайного вопроса из словаря
#
#####################################################################

import logging
import argparse
import random
from os import walk as walkpath
from os.path import join as joinpath



logger = logging.getLogger(__file__)


def get_random_file(files_dir):
	paths_files = []
	for root, dirs, files in walkpath(files_dir):
		for filename in files:
			paths_files.append(joinpath(root, filename))
	file_number = random.randrange(len(paths_files))
	return paths_files[file_number]

def parsing_file(file):
	with open(file, 'r', encoding='KOI8-R') as my_file:
		question_data = my_file.read()
	chunks = question_data.split('\n\n')

	cleaned_chunks = []

	for chunk in chunks:
		lines = chunk.split('\n')
		cleaned_lines = []

		for line in lines:
			if line[:6] == 'Вопрос':
				cleaned_line = 'Вопрос:'
			elif 'pic:' in line:
				cleaned_line = 'Здесь должна быть картинка (вот только где она затерялась?)'
			elif line == '':
				cleaned_line = None
			else:
				line_chunks = line.split()
				cleaned_line = ' '.join(line_chunks)
			if cleaned_line:
				cleaned_lines.append(cleaned_line)

		if cleaned_lines:
			key = cleaned_lines[0]
			value = ' '.join(cleaned_lines[1:])
			cleaned_chunks.append([key, value])

	question_cards_from_file = []
	keys = [
		'Вопрос',
		'Ответ',
		'Зачет',
		'Комментарий',
		'Источник',
		'Автор',
	]
	question_card = {key: None for key in keys}

	for chunk in cleaned_chunks:	
		if chunk[0] == 'Вопрос:' and question_card['Вопрос']:
			question_cards_from_file.append(question_card)
			question_card = {key: None for key in keys}

		if chunk[0][:-1] in keys:
			question_card[chunk[0][:-1]] = chunk[1]

	return question_cards_from_file


def get_questions_dict(files_dir):
	question_cards = []
	for root, dirs, files in walkpath(files_dir):
		for filename in files:
			print(root)
			print(filename)
			filename = joinpath(root, filename)
			question_cards_from_file = parsing_file(filename)
			question_cards.extend(question_cards_from_file)

	return question_cards


def main():

	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	parser = argparse.ArgumentParser(
		description='''
		Программа принимает на вход путь до текстового файла с вопросами 
		викторины и возвращает эти вопросы в виде структурированного словаря.
		'''
		)
	parser.add_argument('-f', '--filename', help='имя файла')
	args = parser.parse_args()
	
	try:
		question_cards = parse_file(args.filename)
	except FileNotFoundError:
		logging.error('Ошибка: Файл не найден', exc_info=True)




if __name__ == "__main__":
	main()


