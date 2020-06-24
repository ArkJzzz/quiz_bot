#!/usr/bin/python3
__author__ = 'ArkJzzz (arkjzzz@gmail.com)'



import sys
import logging
# import random

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
logger.setLevel(logging.DEBUG)


database = redis.Redis(
    host=settings.redis_host, 
    port=settings.redis_port, 
    db=settings.redis_db_number, 
    password=settings.redis_password,
)

CHOOSING, TYPING_REPLY = range(2)

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
    text='Привет, это бот для викторин!'

    context.bot.send_message(
        chat_id=chat_id,
        text=text, 
        reply_markup=REPLY_MARKUP
    )

    return CHOOSING

def new_question(update, context):
    question_card_number = quiz_tools.get_random_question_card_number(database)
    question_card = redis_tools.get_value_from_database(
            key=question_card_number, 
            database=database,
        )
    chat_id = update.effective_chat.id
    quiz_tools.add_user_to_database(
            chat_id=chat_id,
            source='tg',
            value=question_card_number,
            database=database,
        )
    logger.debug(
        'user: {id}, question_card_number: {cq_number}'.format(
            id=chat_id,
            cq_number=question_card_number
        )
    )
    question = question_card['question']
    update.message.reply_text(
        text=question,
        # reply_markup=REPLY_MARKUP,
    )   
    logger.debug(question_card)

    return CHOOSING


def capitulate(update, context):
    chat_id = update.effective_chat.id
    last_asked_question = quiz_tools.get_last_asked_question(
        chat_id=chat_id, 
        source='tg', 
        database=database,
        )
    answer = quiz_tools.get_long_answer(last_asked_question, database)
    logger.debug(answer)




    # question_card = quiz_tools.get_dict_value(
    #     key=last_asked_question, 
    #     database=database,
    # )

    # full_answer = question_card['Полный ответ']

    update.message.reply_text(
        text=answer,
        reply_markup=REPLY_MARKUP,
    )

    return CHOOSING


def received_information(update, context):
    logger.debug('received_information')
    # user_data = context.user_data
    text = update.message.text
    logger.debug(text)

    # update.message.reply_text(
    #     'Вы ответили: {}'.format(text),
    #     reply_markup=REPLY_MARKUP,
    # )

    return CHOOSING


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    # database = redis.Redis(
    #     host=settings.redis_host, 
    #     port=settings.redis_port, 
    #     db=settings.redis_db_number, 
    #     password=settings.redis_password,
    # )

    files_dir = settings.quiz_question_dir
    logger.debug('Files dir: {}'.format(files_dir))



    updater = Updater(
        settings.telegram_token, 
        use_context=True,
    )
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start,),
        ],

        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Новый вопрос)$'),
                    new_question,
                ),
                MessageHandler(
                    Filters.regex('^(Сдаться)$'),
                    capitulate,
                ),
                MessageHandler(
                    Filters.text, 
                    received_information,
                ),
            ],

            TYPING_REPLY: [
                MessageHandler(
                    Filters.text, 
                    received_information,
                ),
            ],
        },

        fallbacks=[]
    )

    updater.dispatcher.add_handler(conv_handler)

    try:
        # question_cards = quiz_tools.get_question_cards(files_dir)
        # quiz_tools.add_question_cards_to_database(
        #         question_cards, 
        #         database,
        #     )

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


