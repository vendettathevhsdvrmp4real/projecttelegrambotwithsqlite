from logic import *
from config import *
from logic2 import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import time
import random

bot = TeleBot(API_TOKEN)

db = DatabaseManager(DATABASE)

@bot.message_handler(commands=['start'])
def start_handler(message):
        bot.send_message(message.chat.id, "👋 Привет! Это служба поддержки [Название вашего бота/сервиса]. Пожалуйста, опишите ваш вопрос/проблему в одном сообщении. Наши операторы работают с [Указать время работы, например: test].")
        bot.send_message(message.chat.id, "Но для начало, мне нужно сказать твоё имя для тех поддержка")
        bot.send_message(message.chat.id, "Введите своё имя")
        time.sleep(3)
        bot.register_next_step_handler(message,register2)

def register2(message):
    telegram_id = message.from_user.id  # id пользователя
    name = message.text.strip()         # текст сообщения

    try:
        # Попытка сохранить пользователя в БД
        db.save_user(telegram_id, name)

        # Отправка сообщения об успешном сохранении
        bot.send_message(message.chat.id, f"Отлично, **{name}**! Твоё имя успешно сохранено. 🎉")
        bot.send_message(message.chat.id, f"Приятно познакомиться, {name}!")

    except Exception as e:
        # В случае ошибки выводим сообщение об ошибке
        bot.send_message(message.chat.id, "Произошла ошибка при сохранении данных. Попробуй позже.")
        print(f"Ошибка при сохранении пользователя: {e}")



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Игнорируем команды, они обрабатываются другими хэндлерами
    if message.text.startswith('/'):
        return

    user_text = message.text.strip()
    answer = get_answer(user_text)

    if answer:
        bot.reply_to(message, f"Ответ: {answer}")
    else:
        bot.reply_to(message, "Извини, я не нашёл ответ на этот вопрос")

@bot.message_handler(commands=['help'])
def help_command(message):
     bot.reply_to(message, "/contact - Связаться с поддержкой ")

@bot.message_handler(commands=['contact'])
def contact_command(message):
     bot.reply_to(message, "Вы можете связаться с нашей поддержкой, выбрав один из вариантов ниже:")
     bot.reply_tO(message, "@") #insert your tg username

if __name__ == '__main__':
    manager = DatabaseManager(DATABASE)
    bot.infinity_polling()