import telebot
import psycopg2
from telebot import types
from aiogram import types

bot = telebot.TeleBot('5650881009:AAEY49IpxG6qd4jku5y37dXQW3NMmin2Zr4')
DB_URI = 'jdbc:postgresql://localhost:5432/postgres'
db_conection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_conection.cursor()



@bot.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Покажи меню")
    btn2 = types.KeyboardButton("❓ Задати питання")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привiт, {0.first_name}!".format(message.from_user), reply_markup=markup, disable_web_page_preview=True, parse_mode="html")

    db_object.execute(f"SELECT ID FROM users WHERE id = {id}")
    result = db_object.fetchone()
    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s, %s, %s)", (id, 0))
        db_conection.commit()

    @bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
    def get_text_messages(message):


        if message.text == "Привіт":
            bot.send_message(message.chat.id, "Привiт, чим я можу тобi допомогти?")

        elif message.text == "Покажи меню":
            p = open("5d7c27d23be68.jpeg", "rb")
            bot.send_photo(message.chat.id, p)

        elif message.text == "👋 Покажи меню":
            p = open("5d7c27d23be68.jpeg", "rb")
            bot.send_photo(message.chat.id, p)

        elif message.text == "/help":
            bot.send_message(message.chat.id, "Напиши привiт")

        elif message.text == "❓ Задати питання":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Як тебе звати?")
            btn2 = types.KeyboardButton("Що ти вмієш?")
            back = types.KeyboardButton("Вернутись в головне меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

        elif message.text == "Як тебе звати?":
            bot.send_message(message.chat.id, "В мене нема імені..")

        elif message.text =="Що ти вмієш?":
            bot.send_message(message.chat.id, text="Показувати меню")


        elif message.text == "Вернутись в головне меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("👋 Покажи меню")
            button2 = types.KeyboardButton("❓ Задати питання")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, text="Ви повернулись в головне меню", reply_markup=markup)

        else:
            bot.send_message(message.chat.id, "Я тебе не розумiю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
