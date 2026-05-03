import telebot
import random
import os
from flask import Flask
from threading import Thread

TOKEN = "8304829067:AAF9TM-4GpsSmvvTqzY297rx9yfLH-Gqvc8"  # << ШУ ЕРГА ТОКЕН
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Бот тирик!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

user_numbers = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_numbers[user_id] = random.randint(1, 10)
    bot.send_message(message.chat.id, "Салом! 👋\nМен 1 дан 10 гача сон ўйладим.\nТоп-чи!\n\nЯнги ўйин: /game")

@bot.message_handler(commands=['game'])
def game(message):
    user_id = message.from_user.id
    user_numbers[user_id] = random.randint(1, 10)
    bot.send_message(message.chat.id, "Янги ўйин! 1 дан 10 гача сон ўйладим. Топ-чи!")

@bot.message_handler(func=lambda message: True)
def guess_number(message):
    user_id = message.from_user.id
    if user_id not in user_numbers:
        bot.send_message(message.chat.id, "Аввал /start босинг!")
        return
    
    try:
        guess = int(message.text)
        secret_number = user_numbers[user_id]
        
        if guess == secret_number:
            bot.send_message(message.chat.id, f"УРАА! Топдинг! 🎉\nМен {secret_number} сонини ўйлагандим.\n\nЯна ўйнаш: /game")
            user_numbers[user_id] = random.randint(1, 10)
        elif guess < secret_number:
            bot.send_message(message.chat.id, "Менинг соним каттароқ! 👆")
        else:
            bot.send_message(message.chat.id, "Менинг соним кичикроқ! 👇")
    except ValueError:
        bot.send_message(message.chat.id, "Фақат сон ёзинг! /game босиб янги ўйин бошланг.")

keep_alive()
bot.polling(none_stop=True)