#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging

import redis
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler

import settings
import quiz_tools
import redis_tools

logger = logging.getLogger(__file__)



DATABASE = redis_tools.connect_to_redis()
KEYBOARD = [
    ['Новый вопрос'],
    ['Сдаться'],
]
REPLY_MARKUP = ReplyKeyboardMarkup(
    KEYBOARD, 
    resize_keyboard=True,
    one_time_keyboard=False,
)


def start(update, context):
    logger.debug('new start')
    chat_id=update.effective_chat.id
    text='Привет, это бот для викторин!\nНажми "Новый вопрос", чтобы начать.'
    context.bot.send_message(
        chat_id=chat_id,
        text=text, 
        reply_markup=REPLY_MARKUP
    )


def handle_new_question(update, context):
    question_card_number = quiz_tools.get_random_question_card_number(DATABASE)
    question_card = redis_tools.get_value_from_database(
            key=question_card_number, 
            database=DATABASE,
        )
    chat_id = update.effective_chat.id
    quiz_tools.add_user_to_database(
            chat_id=chat_id,
            source='tg',
            value=question_card_number,
            database=DATABASE,
        )
    logger.debug(
        'user: {}\nquestion_card_number: {}\n{}'.format(
            chat_id,
            question_card_number,
            question_card,
        )
    )
    question = question_card['question']
    update.message.reply_text(
        text=question,
        reply_markup=REPLY_MARKUP,
    )   


def handle_capitulate(update, context):
    chat_id = update.effective_chat.id
    last_asked_question = quiz_tools.get_last_asked_question(
        chat_id=chat_id, 
        source='tg', 
        database=DATABASE,
        )
    answer = quiz_tools.get_long_answer(last_asked_question, DATABASE)
    update.message.reply_text(
        text=answer,
        reply_markup=REPLY_MARKUP,
    )


def handle_answer_attempt(update, context):
    chat_id = update.effective_chat.id
    user_answer = update.message.text
    verdict = quiz_tools.evaluate_answer(
            user_answer=user_answer, 
            chat_id=chat_id, 
            source='tg', 
            database=DATABASE,
        )
    update.message.reply_text(
        text=verdict,
        reply_markup=REPLY_MARKUP,
    )


def main():
    logger.setLevel(logging.DEBUG)
    
    updater = Updater(
        settings.telegram_token, 
        use_context=True,
    )
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                'start', 
                start,
            ),
            MessageHandler(
                Filters.regex('^(Новый вопрос)$'),
                handle_new_question,
            ),
            MessageHandler(
                Filters.regex('^(Сдаться)$'),
                handle_capitulate,
            ),
            MessageHandler(
                Filters.text, 
                handle_answer_attempt,
            ),

        ],

        states={},
        fallbacks=[]
    )

    updater.dispatcher.add_handler(conv_handler)

    try:
        logger.debug('Стартуем бота')
        updater.start_polling()

    except FileNotFoundError:
        logger.error('Ошибка: Файл не найден', exc_info=True)
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


