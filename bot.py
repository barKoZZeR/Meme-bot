import random
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

user_memes = {}


# Функция для получения всех мемов с нескольких страниц сайта memify.ru
def get_all_memes(pages=10):
    memes = []
    base_url = 'https://www.memify.ru/top/?page='

    for page in range(1, pages + 1):
        url = f'{base_url}{page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        meme_container = soup.find('div', class_='meme-list infinite-container')

        meme_links = meme_container.find_all('a', href=True)

        for link in meme_links:
            if link['href'].startswith('https://www.cdn.memify.ru'):
                memes.append(link['href'])

    return memes


def get_random_meme(user_id):
    all_memes = get_all_memes()

    if user_id not in user_memes:
        user_memes[user_id] = []

    available_memes = list(set(all_memes) - set(user_memes[user_id]))

    if not available_memes:
        user_memes[user_id] = []
        available_memes = all_memes

    random_meme = random.choice(available_memes)

    user_memes[user_id].append(random_meme)

    return random_meme


def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Получить мем", callback_data='get_meme')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Привет! Нажми на кнопку, чтобы получить мем.', reply_markup=reply_markup)


def button(update: Update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'get_meme':
        user_id = query.from_user.id
        meme_url = get_random_meme(user_id)

        query.message.reply_photo(meme_url)

        keyboard = [[InlineKeyboardButton("Получить мем", callback_data='get_meme')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.message.reply_text('Нажми на кнопку, чтобы получить ещё один мем!', reply_markup=reply_markup)


def main():
    TOKEN = 'TOKEN_FROM_BOTFATHER'

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()