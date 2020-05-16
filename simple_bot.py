# coding=utf-8
from telegram import Update, Bot, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.utils.request import Request

from db_utils import *
from common_utils import *

TG_TOKEN = "1177822581:AAEOo_kUnjleDhvgvLyTsdBsADllYnskp4k"
button_key = "Хочу ключ"
button_cat = "Хочу кота"

reply_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=button_key),
        ],
        [
            KeyboardButton(text=button_cat),
        ],
    ],
    resize_keyboard=True,
)


@log_error
def button_cat_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='<^- _ -^>',
        reply_markup=reply_markup
    )


@log_error
def button_key_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    has_key = check_user_has_key(user_id=user_id)
    if has_key:
        booked_key = return_key_by_user_id(user_id=user_id)
        reply_text = f'''
Ключ для голосования можно взять только один раз. Многоразовый у нас только кот.\n\n
Твой ключ-псевдоним на этот вечер: '{booked_key}'.\n\n
Скопируй его в гугл форму для голосования.\n
Ключи помогут сделать наше голосование честным и прозрачным.\n
По ключу ты сможешь проверить как был учтен твой голос.'''
    else:
        random_id = get_random_free_id()
        book_free_key(user_id=user_id, id=random_id)
        new_random_key = return_key_by_id(id=random_id)
        print(f'Выбран случайный id: {random_id}')
        print(f'Получен ключ: {new_random_key}')
        print(f'Список id свободных ключей: {get_free_key_ids()}')
        reply_text = f'''
Забирай)\n\n
Твой ключ-псевдоним на этот вечер: '{new_random_key}'.\n\n
Скопируй его в гугл форму для голосования.\n
Ключи помогут сделать наше голосование честным и прозрачным.\n
По ключу ты сможешь проверить как был учтен твой голос.'''

    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_markup
    )


@log_error
def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'anonymus'

    text = update.effective_message.text
    reply_text = f'Привет, {name}!'

    if text == button_cat:
        return button_cat_handler(update=update, context=context)

    if text == button_key:
        return button_key_handler(update=update, context=context)

    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_markup,
    )


def main():
    print('Start')

    req = Request(
        connect_timeout=1.0,
        read_timeout=1.0,
    )
    bot = Bot(
        request=req,
        token=TG_TOKEN,
        base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    print(f'Bot info: {info}')

    # Подключиться к СУБД
    init_db(force=True)
    fill_db()
    print(f'Количество ключей в базе: {count_keys()}')
    print(f'Количество свободных ключей в базе: {count_free_keys()}')
    print(f'Список ключей: \n{list_keys()}')

    handler = MessageHandler(filters=Filters.all, callback=message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()
    print('End')


if __name__ == '__main__':
    main()
