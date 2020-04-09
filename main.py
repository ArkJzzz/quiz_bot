#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import os
import logging
import argparse
from os.path import isfile
from os.path import join as joinpath
from parse_file import get_chunks_from_file
from parse_file import get_list_cleaned_chunks
from parse_file import get_questions
from parse_file import print_question


logger = logging.getLogger(__file__)


def main():
	# init
	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	quiz_questions_dir = 'quiz-questions/'
	# test

	try:
		for file in os.listdir(quiz_questions_dir):
			file = joinpath(quiz_questions_dir, file)
			if isfile(file):
				chunks = get_chunks_from_file(file)
				cleaned_chunks = get_list_cleaned_chunks(chunks)
				questions = get_questions(cleaned_chunks)
				for question in questions:
					print_question(question)
	except FileNotFoundError:
		logging.error('Ошибка: Файл не найден', exc_info=True)


if __name__ == "__main__":
	main()


