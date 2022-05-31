# -*- coding: utf-8 -*-

import telebot
from telebot import types

TOKEN = '1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0'

OPTIONS = {
    "СГН3-61Б": 0,
    "СГН3-62Б": 0,
    "СГН3-63Б": 0,
    "СГН3-64Б": 0,
}


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    sendDefaultKeyBoard(message.chat.id)

@bot.callback_query_handler(func=lambda message: message.data)
def button(message):
    if message.data in OPTIONS:
        OPTIONS[message.data] += 1
        OPTIONS[message.data + randomword(3)] = 0
        sendKeyBoard(message.message.chat.id, message.data + "\n" + "На эту кнопку нажали " + str(OPTIONS[message.data]) + " раз(а).", OPTIONS.keys())

def sendKeyBoard(chatId, message, buttons):
    keyboard = types.InlineKeyboardMarkup()

    for button in buttons:
        keyboard.row(types.InlineKeyboardButton(text = button, callback_data= button))

    bot.send_message(chatId, message, reply_markup=keyboard)

def sendDefaultKeyBoard(chatId):
    sendKeyBoard(chatId, "Проголосуй", OPTIONS.keys())


import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

bot.polling(none_stop=True)