#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging
import argparse


logger = logging.getLogger(__file__)

def get_chunks_from_file(file):
	with open(file, 'r', encoding='KOI8-R') as my_file:
		question_data = my_file.read()
	chunks = question_data.split('\n\n')
	return chunks


def get_list_cleaned_chunks(chunks):
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

	return cleaned_chunks


def get_questions(chunks_list):
	questions = []
	keys = [
		'Вопрос',
		'Ответ',
		'Зачет',
		'Комментарий',
		'Источник',
		'Автор',
	]
	question = question = {key: None for key in keys}

	for item in chunks_list:	
		if item[0] == 'Вопрос:' and question['Вопрос']:
			questions.append(question)
			question = {key: None for key in keys}

		if item[0][:-1] in keys:
			question[item[0][:-1]] = item[1]

	return questions


def print_question(question):
	for key, value in question.items():
		print('{} - {}'.format(
			key,
			value,
			)
		)
	print()


def main():
	# init
	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	# do
	parser = argparse.ArgumentParser(
		description='''
		Программа принимает на вход путь до текстового файла с вопросами викторины 
		и возвращает эти вопросы в виде структурированного словаря.
		'''
		)
	parser.add_argument('-f', '--filename', help='имя файла')
	args = parser.parse_args()
	
	try:
		chunks = get_chunks_from_file(args.filename)
		cleaned_chunks = get_list_cleaned_chunks(chunks)
		questions = get_questions(cleaned_chunks)
	except FileNotFoundError:
		logging.error('Ошибка: Файл не найден', exc_info=True)


	# test
	for question in questions:
		print_question(question)

if __name__ == "__main__":
	main()


