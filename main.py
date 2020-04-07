#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging


logger = logging.getLogger(__file__)


def clear_junk(line):
	if line == '':
		return None
	elif 'pic:' in line:
		new_line = 'Здесь должна быть картинка (вот только где она затерялась?)'
		return new_line
	elif line[:6] == 'Вопрос':
		new_line = 'Вопрос:'
		return new_line
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
			idx = lines.index(line)
			cleaned_line = clear_junk(line)
			if cleaned_line:
				cleaned_lines.append(cleaned_line)

		if cleaned_lines:
			key = cleaned_lines[0]
			value = ' '.join(cleaned_lines[1:])
			cleaned_chunks.append([key, value])

	return cleaned_chunks


def main():
	# init

	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	# do
	question = {}
	questions_list = []
	answers_list = []
	comments_list = []

	with open('quiz-questions/3tela18.txt', 'r', encoding='KOI8-R') as my_file:
		chunks = my_file.read()

	chunks = chunks.split('\n\n')
	cleaned_chunks = get_list_cleaned_chunks(chunks)

	for key, value in cleaned_chunks:
		logger.debug('\n{}\n{}'.format(key, value))


	# question = {
	# 	'Вопрос': None, 
	# 	'Ответ': None, 
	# 	'Зачет': None, 
	# 	'Комментарий': None, 
	# 	'Источник': None, 
	# 	'Автор': None,
	# }

if __name__ == "__main__":
	main()
