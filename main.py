#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging


logger = logging.getLogger(__file__)


def main():
	# init

	logging.basicConfig(
		format='\n%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
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
	new_chunks = []

	question = {
		'Вопрос': None, 
		'Ответ': None, 
		'Зачет': None, 
		'Комментарий': None, 
		'Источник': None, 
		'Автор': None,
	}
	
	for chunk in chunks:
		chunk_lines = chunk.split('\n')

		for line in chunk_lines:
			idx = chunk_lines.index(line)
			line_chunks = line.split()
			new_line = ' '.join(line_chunks)
			chunk_lines.remove(line)

			if line[:6] == 'Вопрос':
				chunk_lines.remove(line)
				chunk_lines.insert(idx, 'Вопрос:')

			if 'pic:' in line:
				chunk_lines.remove(line)

			if line == '':
				chunk_lines.remove(line)

			chunk_lines.insert(idx, new_line)


		# for line in chunk_lines:
		# 	idx = chunk_lines.index(line)
		# 	line_chunks = line.split()
		# 	new_line = ' '.join(line_chunks)
		# 	chunk_lines.remove(line)
		# 	chunk_lines.insert(idx, new_line)
			
		logger.debug('{}'.format(chunk_lines))






		key = chunk_lines[0]
		value = ' '.join(chunk_lines[1:])
		logger.debug('{}'.format(value))
		question = (key, value)
		new_chunks.append(question)




		# if 'Источник:' in x:
		# 	pass
		# elif 'Автор:' in x:
		# 	pass
		# else:
		# 	questions_list.append(chunk)

	# for chunk in new_chunks:
	# 	logger.debug('{}'.format(chunk))

	# for x in range(len(questions_list)-2):
	# 	logger.debug('{}'.format(questions_list[x]))
	# 	logger.debug('{}'.format(answers_list[x]))
	# 	logger.debug('{}'.format(comments_list[x]))


if __name__ == "__main__":
	main()


# Вопрос 11:
# В одной из песен Тома ЛЕрера есть слово "margin" [мАрджин], означающее
# поля книги. С фамилией какого англичанина в этой песне рифмуется слово
# "улыбается"?

# Ответ:
# Уайлс.

# Комментарий:
# Слово "smiles" [смайлс] рифмуется с фамилией "Wiles" [уАйлс] - как вы
# помните, Эндрю Уайлс доказал теорему Ферма, которую сам Ферма
# сформулировал на полях "Арифметики" Диофанта.

# Источник:
# https://genius.com/Tom-lehrer-thats-mathematics-lyrics

# Автор:
# Павел Семенюк (Гринфилд - Москва)

# Вопрос 12:
# Одно из преобразований числовых последовательностей включает в себя
# построение треугольной таблицы сверху вниз и заполнение ее по следующему
# правилу: в четных строках следующее число равно сумме числа слева и
# слева выше, а в нечетных - справа и справа выше. Каким словом греческого
# происхождения называется это преобразование?

# Ответ:
# Бустрофедон.

# Комментарий:
# Четные строки заполняются слева направо, а нечетные - справа налево.
# Таким же образом организован способ письма "бустрофедон", название
# которого происходит от греческих слов со значениями "бык" и
# "поворачиваю".

# Источник:
# https://ru.wikipedia.org/wiki/Бустрофедонное_преобразование

# Автор:
# Павел Семенюк (Гринфилд - Москва)

# Тур:
# 3 тур

# Вопрос 1:
# В статье "Теория струн для чайников" для объяснения того, почему
# некоторые физические абстракции невозможно себе представить, автор
# приводит в пример жителей... Какой страны?

# Ответ:
# Флатландия.

# Комментарий:
# Как жители плоской страны не могут представить себе обыденное для нас
# третье измерение, так и нашему разуму сложно вообразить скрытые семь,
# которыми оперирует теория струн.

# Источник:
# https://masterok.livejournal.com/2250699.html

# Автор:
# Сергей Дуликов (Брянск - Москва)

# Вопрос 2:
# (pic: 20180366.jpg)
#    Этот вопрос не по физике.
#    Напишите фамилию человека, изображенного на раздаточном материале.

# Ответ:
# Резерфорд.

# Комментарий:
# Известное выражение Резерфорда: "Наука - это либо физика, либо коллекционирование марок".

# Источник:
# https://ru.wikipedia.org/wiki/Файл:The_Soviet_Union_1971_CPA_4043_stamp_(Ernest_Rutherford_and_Diagram_of_Rutherford_Scattering).jpg

# Автор:
# Сергей Дуликов (Брянск - Москва)
