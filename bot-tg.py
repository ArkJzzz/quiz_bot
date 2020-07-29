#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import logging

import redis
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler

import settings
import quiz_tools
import redis_tools

logger = logging.getLogger('bot_tg')


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
    chat_id = update.effective_chat.id
    question_card_number = quiz_tools.get_random_question_card_number(DATABASE)
    quiz_tools.add_userdata_to_database(
            chat_id=chat_id,
            source='tg',
            question_card_number=question_card_number,
            database=DATABASE,
        )
    question = quiz_tools.get_question(question_card_number, DATABASE)
    update.message.reply_text(
        text=question,
        reply_markup=REPLY_MARKUP,
    )   


def handle_capitulate(update, context):
    chat_id = update.effective_chat.id
    question_card_number = quiz_tools.get_last_asked_question(
            chat_id=chat_id,
            source='tg',
            database=DATABASE,
        )
    answer = quiz_tools.get_long_answer(question_card_number, DATABASE)
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


def error_handler(update: Update, context: CallbackContext):
    try:
        raise context.error
    except FileNotFoundError:
        logger.error('Ошибка: Файл не найден', exc_info=True)
    except redis.exceptions.AuthenticationError:
        logger.error('Подключение к базе данных: ошибка аутентификации')
    except Exception  as err:
        logger.error('Бот упал с ошибкой:')
        logger.error(err)
        logger.debug(err, exc_info=True)





def main():
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
    updater.dispatcher.add_error_handler(error_handler)

    logger.debug('Стартуем бота')
    updater.start_polling()
    updater.idle()
    logger.info('Бот остановлен')

if __name__ == "__main__":
    main()


