import os

import telebot

bot = telebot.TeleBot(
    os.environ['NASHENAS_BOT_TOKEN'], parse_mode='HTML'
)
