import os
import telebot
from telebot import types
from dotenv import load_dotenv

from auth import auth

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Отправить контакт", request_contact=True))
    bot.send_message(message.from_user.id, "Привет! Здесь ты сможешь обменять свои CTFCoin'ы на наш мерч;) Но сначала нужно авторизоваться, пришли в ответ свой контакт", reply_markup=markup)

@bot.message_handler(content_types=['text','contact'])
def get_text_messages(message):
    if message.contact is not None:
        answer = auth(message)
        bot.send_message(message.from_user.id, answer, reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть