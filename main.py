import telebot
from telebot import types

import auth

# bot = telebot.TeleBot(os.getenv("TOKEN"))
bot = telebot.TeleBot("")

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Отправить контакт", request_contact=True))
    bot.send_message(message.from_user.id, "Привет! Здесь ты сможешь обменять свои CTFCoin'ы на наш мерч;) Но сначала нужно авторизоваться, пришли в ответ свой контакт", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message)

    if message.contact is not None:
        answer = auth(message)
        bot.send_message(message.from_user.id, answer)

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть