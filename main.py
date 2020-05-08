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
from telegram.ext import ConversationHandler

from quiz_tools import get_questions_dict


logger = logging.getLogger(__file__)
load_dotenv()
BASE_DIR = dirname(abspath(__file__))
QUIZ_QUESTION_DIR = 'quiz-questions'
QUIZ_QUESTION_DIR = joinpath(BASE_DIR, QUIZ_QUESTION_DIR)
QUESTION_CARDS = get_questions_dict(QUIZ_QUESTION_DIR)
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
DB = redis.Redis(
		host=getenv('REDIS_HOST'), 
		port=getenv('REDIS_PORT'), 
		db=0, 
		password=getenv('REDIS_PASSWORD'),
	)

CHOOSING, TYPING_REPLY = range(2)

keyboard = [
	['Новый вопрос'],
	['Сдаться'],
]
reply_markup = ReplyKeyboardMarkup(keyboard)


def start(update, context):
	logger.debug('startbot_handler')
	chat_id=update.effective_chat.id
	text='Привет, это бот для викторин!'

	context.bot.send_message(
		chat_id=chat_id,
		text=text, 
		reply_markup=reply_markup
	)

def handle_new_question_request(update, context):
	chat_id = update.effective_chat.id
	question_card_number = random.randrange(len(QUESTION_CARDS))
	question_card = QUESTION_CARDS[question_card_number]
	DB.set(chat_id, question_card_number)
	new_question = question_card['Вопрос']
	update.message.reply_text(new_question)

	logger.debug('выбрана карточка: {}'.format(question_card))
	logger.debug('chat_id: {chat_id}, question_card_number: {question_card_number}'.format(
		chat_id=chat_id,
		question_card_number=(DB.get(chat_id)).decode('utf-8'), 
		)
	)

	return TYPING_REPLY


def handle_solution_attempt(update, context):
	chat_id = update.effective_chat.id
	question_card_number = (DB.get(chat_id)).decode('utf-8')
	question_card_number = int(question_card_number)
	question_card = QUESTION_CARDS[question_card_number]
	correct_answer = [
		question_card['Ответ'],
		question_card['Комментарий'],
		question_card['Источник'],
	]

	excluded_characters = ['.', ',', '!', '?', '[', ']', '(', ')']
	answer = message_text.lower()
	correct_answer = correct_answer[0].lower()
	for character in excluded_characters:
		answer = answer.replace(character, ' ')
		correct_answer = correct_answer.replace(character, ' ')
	if correct_answer[1]:
		ofset = correct_answer[1].lower()
	if answer in (correct_answer, ofset):
		update.message.reply_text('Правильно! Для следующего вопроса нажми «Новый вопрос»')
	else:
		update.message.reply_text('Неправильно... Попробуешь ещё раз?')
	
	return CHOOSING



def handle_capitulate(update, context):
	chat_id = update.effective_chat.id
	question_card_number = (DB.get(chat_id)).decode('utf-8')
	question_card_number = int(question_card_number)
	question_card = QUESTION_CARDS[question_card_number]
	correct_answer = [
		question_card['Ответ'],
		question_card['Комментарий'],
		question_card['Источник'],
	]
	for chunk in correct_answer:
		if chunk:
			update.message.reply_text(chunk)

	return CHOOSING


def regular_choice(update, context):
	chat_id = update.effective_chat.id
	message_text = update.message.text
	if message_text == 'Новый вопрос':
		new_qwestion = get_new_question(chat_id)
		update.message.reply_text(new_qwestion)
	elif message_text == 'Мой счет':
		score = get_score(chat_id)
		update.message.reply_text(score)
	elif message_text == 'Сдаться':
		correct_answer = get_correct_answer(chat_id)
		for chunk in correct_answer:
			if chunk:
				update.message.reply_text(chunk)
	else:
		correct_answer = get_correct_answer(chat_id)
		evaluation_result = evaluate_answer(correct_answer, message_text)
		update.message.reply_text(evaluation_result)


def get_new_question(chat_id):
	question_card_number = random.randrange(len(QUESTION_CARDS))
	question_card = QUESTION_CARDS[question_card_number]
	new_question = question_card['Вопрос']
	DB.set(chat_id, question_card_number)

	logger.debug('выбрана карточка: {}'.format(question_card))
	logger.debug('chat_id: {chat_id}, question_card_number: {question_card_number}'.format(
		chat_id=chat_id,
		question_card_number=(DB.get(chat_id)).decode('utf-8'), 
		)
	)

	return new_question


def get_score(chat_id):
	score = 'Здесь тебе не банк!'
	return score


def get_correct_answer(chat_id):
	question_card_number = (DB.get(chat_id)).decode('utf-8')
	question_card_number = int(question_card_number)
	question_card = QUESTION_CARDS[question_card_number]
	correct_answer = [
		question_card['Ответ'],
		question_card['Комментарий'],
		question_card['Источник'],
	]
	return correct_answer


def evaluate_answer(correct_answer, message_text):
	excluded_characters = ['.', ',', '!', '?', '[', ']', '(', ')']
	answer = message_text.lower()
	correct_answer = correct_answer[0].lower()
	for character in excluded_characters:
		answer = answer.replace(character, ' ')
		correct_answer = correct_answer.replace(character, ' ')
	if correct_answer[1]:
		ofset = correct_answer[1].lower()
	if answer in (correct_answer, ofset):
		evaluation_result = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
	else:
		evaluation_result = 'Неправильно... Попробуешь ещё раз?'
	return evaluation_result


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

	conversation_handler = ConversationHandler(
		entry_points=[
			CommandHandler('start', start),
			MessageHandler(
				Filters.regex('^Новый вопрос$'),
				handle_new_question_request,
			),	
			MessageHandler(
				Filters.regex('^Сдаться$'),
				handle_capitulate,
				),
			MessageHandler(
				Filters.text,
				handle_solution_attempt,
			)
		],
		states={},
		fallbacks=[],
	)

	dp.add_handler(conversation_handler)
	# dp.add_handler(CommandHandler('start', start_bot))
	# dp.add_handler(MessageHandler(Filters.text, regular_choice))



	try:
		logger.debug('Стартуем бота')
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


