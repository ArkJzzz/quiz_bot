#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging


logger = logging.getLogger(__file__)


def clear_junk(line):
	if line[:6] == 'Вопрос':
		new_line = 'Вопрос:'
		return new_line
	elif 'pic:' in line:
		new_line = 'Здесь должна быть картинка (вот только где она затерялась?)'
		return new_line
	# elif line == '':
	# 	return None
	else:
		line_chunks = line.split()
		new_line = ' '.join(line_chunks)
		return new_line


def get_list_cleaned_chunks(chunks):
	cleaned_chunks = []

	for chunk in chunks:
		lines = chunk.split('\n')
		cleaned_lines = []

		for line in lines:
			cleaned_line = clear_junk(line)
			if cleaned_line:
				cleaned_lines.append(cleaned_line)

		if cleaned_lines:
			key = cleaned_lines[0]
			value = ' '.join(cleaned_lines[1:])
			cleaned_chunks.append([key, value])

	return cleaned_chunks


def get_questions(chunks_list):
	questions = []
	for line in chunks_list:

		if line[0] == 'Вопрос:':
			question = {'Вопрос': line[1]}
		if line[0] == 'Ответ:':
			question['Ответ']= line[1]
		if line[0] == 'Зачет:':
			question['Зачет']= line[1]
		if line[0] == 'Комментарий:':
			question['Комментарий']= line[1]
		if line[0] == 'Источник:':
			question['Источник']= line[1]
		if line[0] == 'Автор:':
			question['Автор']= line[1]
			questions.append(question)

	return questions




def main():
	# init
	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	# do
	file = 'quiz-questions/3tela18.txt'
	with open(file, 'r', encoding='KOI8-R') as my_file:
		question_data = my_file.read()

	lines = question_data.split('\n')
	clean_lines = []

	for line in lines:
		clean_line = clear_junk(line)
		clean_lines.append(clean_line)
	
	for line in clean_lines:
		print(line)

	# chunks = question_data.split('\n\n')

	# cleaned_chunks = get_list_cleaned_chunks(chunks)

	# questions = get_questions(cleaned_chunks)

	# for question in questions:
	# 	logger.debug('{}\n{}\n{}'.format(
	# 		question['Вопрос'],
	# 		question['Ответ'],
	# 		question['Комментарий'],
	# 		)
	# 	)

if __name__ == "__main__":
	main()


	# question = {
	# 	'Вопрос': None, 
	# 	'Ответ': None, 
	# 	'Зачет': None, 
	# 	'Комментарий': None, 
	# 	'Источник': None, 
	# 	'Автор': None,
	# }
