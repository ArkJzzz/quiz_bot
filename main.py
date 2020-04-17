#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

#################
##### TODO ######

# Переделать quiz-tools: 
#	возвратить один словарь из всех вопросов из всех файлов
# Вынести quiz-tools в отдельный файл
# Выбор случайного вопроса из словаря
# Оцените ответ пользователя 
# Воспользуйтесь ConversationHandler 
# Добавьте возможность сдаться 



import sys
import logging
import argparse
import random
from os import getenv
from os import listdir
from os import walk as walkpath
from os.path import isfile
from os.path import dirname
from os.path import abspath
from os.path import join as joinpath

import redis
from dotenv import load_dotenv
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler

logger = logging.getLogger(__file__)
load_dotenv()
BASE_DIR = dirname(abspath(__file__))
QUIZ_QUESTION_DIR = 'quiz-questions'
QUIZ_QUESTION_DIR = joinpath(BASE_DIR, QUIZ_QUESTION_DIR)
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

DB = redis.Redis(
		host=REDIS_HOST, 
		port=REDIS_PORT, 
		db=0, 
		password=REDIS_PASSWORD,
	)


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

	for chunk in cleaned_chunks:	
		if chunk[0] == 'Вопрос:' and question_card['Вопрос']:
			question_cards.append(question_card)
			question_card = {key: None for key in keys}

		if chunk[0][:-1] in keys:
			question_card[chunk[0][:-1]] = chunk[1]

	return question_cards

def get_random_question_card(question_cards):
	question_card_number = random.randrange(len(question_cards))
	return question_cards[question_card_number]



def start_bot(update, context):
	logger.debug('startbot_handler')
	chat_id=update.effective_chat.id
	text='Привет, это бот для викторин!'
	keyboard = [
		['Новый вопрос'],
		['Мой счет', 'Сдаться'],
	]
	reply_markup = ReplyKeyboardMarkup(keyboard)

	context.bot.send_message(
		chat_id=chat_id,
		text=text, 
		reply_markup=reply_markup
	)

def get_choise(update, context):
	chat_id = update.effective_chat.id
	message_text = update.message.text
	if message_text == 'Новый вопрос':
		question_cards_file = get_random_file(QUIZ_QUESTION_DIR)	
		question_cards = parsing_file(question_cards_file)
		question_card = get_random_question_card(question_cards)
		question = question_card['Вопрос']
		DB.set(chat_id, question)

		logger.debug('выбран файл: {}'.format(question_cards_file))
		logger.debug('выбран вопрос: {}'.format(question_card))
		logger.debug('chat_id: {chat_id}, qw: {question}'.format(
			chat_id=chat_id,
			question=(DB.get(chat_id)).decode('utf-8'), 
			)
		)

		update.message.reply_text(question)

	if message_text == 'Мой счет':
		update.message.reply_text('Здесь тебе не банк!')

	if message_text == 'Сдаться':
		question = (DB.get(chat_id)).decode('utf-8')
		answer = None # взять ответ по вопросу из словаря.
		update.message.reply_text(question_card['Ответ'])



def main():
	# init
	logging.basicConfig(
		format='%(asctime)s %(name)s - %(funcName)s:%(lineno)d - %(message)s', 
		datefmt='%Y-%b-%d %H:%M:%S (%Z)',
	)
	logger.setLevel(logging.DEBUG)

	updater = Updater(
		token=TELEGRAM_TOKEN, 
		use_context=True, 
	)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start', start_bot))
	dp.add_handler(MessageHandler(Filters.text, get_choise))

	
	# question_cards_file = get_random_file(QUIZ_QUESTION_DIR)
	# question_cards = parsing_file(question_cards_file)
	# question_card = get_random_question_card(question_cards)


	try:


		updater.start_polling()


	except FileNotFoundError:
		logger.error('Ошибка: Файл не найден', exc_info=True)
	# except telegram.error.NetworkError:
	# 	logger.error('Не могу подключиться к telegram')
	except redis.exceptions.AuthenticationError:
		logger.error('Подключение к базе данных: ошибка аутентификации')
	except Exception  as err:
		logger.error('Бот упал с ошибкой:')
		logger.error(err)
		logger.debug(err, exc_info=True)



	updater.idle()
	logger.info('Бот остановлен')

if __name__ == "__main__":
	main()


