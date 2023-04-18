import re
import os
import json
import telebot
from telebot import types
from dotenv import load_dotenv
from peewee import PostgresqlDatabase

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))

db = PostgresqlDatabase(
    os.environ.get('DB_DB'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS'),
    host=os.environ.get('DB_HOST')
)


def webAppKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webApp = types.WebAppInfo("https://loop-lab.github.io/shop/")
    keyboard.add(types.KeyboardButton(text="Веб приложение", web_app=webApp))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Отправить контакт", request_contact=True))
    bot.send_message(
        message.from_user.id,
        "Привет! Здесь ты сможешь обменять свои CTFCoin'ы на наш мерч;) Но сначала нужно авторизоваться, пришли свой контакт",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text','contact'])
def get_text_messages(message):
    if message.contact is not None:
        from models.user import User
        from data_methods import hasActiveOrder
        person = User.get(User.phone == re.findall("\d+", message.contact.phone_number)[0])
        if person is not None:
            if person.tg_id is None:
                person.tg_id = message.from_user.id
                person.save()

            if hasActiveOrder(person.id):
                bot.send_message(message.from_user.id, "У вас уже есть активный заказ, дождитесь его завершения")
            else:
                bot.send_message(message.from_user.id, f"У вас {person.coins} CTFCoin, нажмите на кнопку, чтобы выбрать мерч", reply_markup=webAppKeyboard())
        else:
            bot.send_message(message.from_user.id, "Вы не можете приобрести наш мерч")
    elif message.text == "Да, оплатить!":
        from models.user import User
        from data_methods import updateStatusOrder

        person = User.get(User.tg_id == message.from_user.id)
        if person is not None:
            updateStatusOrder(person.id, 2)

            bot.send_message(message.from_user.id, f"Заказ успешно отправлен в обработку. Мы свяжемся с вами для уточнения деталей")
        else:
            bot.send_message(message.from_user.id, "Вы не можете приобрести наш мерч")
    elif message.text == "Нет":
        from models.user import User
        from data_methods import updateStatusOrder

        person = User.get(User.tg_id == message.from_user.id)
        if person is not None:
            updateStatusOrder(person.id, 4)

            bot.send_message(message.from_user.id, f"Очень жаль, наемся, что в будущем вы приобретете наш мерч")
        else:
            bot.send_message(message.from_user.id, "Вы не можете приобрести наш мерч")
    else:
        bot.send_message(message.from_user.id, f"Я вас не понимаю. Начните диалог заново отправив: /start")

@bot.message_handler(content_types="web_app_data")
def answer(webAppMes):
    order = json.loads(webAppMes.web_app_data.data)
    from data_methods import setOrder, getProductsById, getSizesById

    setOrder(webAppMes.from_user.id, order)
    products = getProductsById([item['id'] for item in order['products']])
    products_by_id = {row['id']: row for row in products}
    sizes = getSizesById([item['size'] for item in order['products']])
    sizes_by_id = {row['id']: row for row in sizes}

    text = "Ваш заказ: "
    for item in order['products']:
        text += f"\n - {products_by_id[item['id']]['name']} ({sizes_by_id[item['size']]['name']}) x{item['count']};"

    text += f"\n\nХотите оплатить?"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Да, оплатить!"))
    markup.add(types.KeyboardButton("Нет"))
    bot.send_message(webAppMes.chat.id, text, reply_markup=markup)

if __name__ == '__main__':
    db.connect()
    bot.infinity_polling()