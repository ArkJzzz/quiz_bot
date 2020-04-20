#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

#####################################################################
# TODO 
#
# 
# Оцените ответ пользователя 
# Воспользуйтесь ConversationHandler 
#####################################################################


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

from quiz_tools import get_questions_dict


logger = logging.getLogger(__file__)
load_dotenv()
BASE_DIR = dirname(abspath(__file__))
QUIZ_QUESTION_DIR = 'quiz-questions'
QUIZ_QUESTION_DIR = joinpath(BASE_DIR, QUIZ_QUESTION_DIR)
QUESTION_CARDS = get_questions_dict(QUIZ_QUESTION_DIR)
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
		question_card_number = random.randrange(len(QUESTION_CARDS))
		question_card = QUESTION_CARDS[question_card_number]
		question = question_card['Вопрос']
		DB.set(chat_id, question_card_number)

		update.message.reply_text(question)

		logger.debug('выбрана карточка: {}'.format(question_card))
		logger.debug('chat_id: {chat_id}, qw: {question}'.format(
			chat_id=chat_id,
			question=(DB.get(chat_id)).decode('utf-8'), 
			)
		)

	if message_text == 'Мой счет':
		update.message.reply_text('Здесь тебе не банк!')

	if message_text == 'Сдаться':
		question_card_number = (DB.get(chat_id)).decode('utf-8')
		question_card_number = int(question_card_number)
		question_card = QUESTION_CARDS[question_card_number]
		answer = question_card['Ответ']
		ofset = question_card['Зачет']
		comment = question_card['Комментарий']
		source = question_card['Источник']
		update.message.reply_text(answer)
		if ofset:
			update.message.reply_text(ofset)
		if comment:
			update.message.reply_text(comment)
		if source:
			update.message.reply_text(source)

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


