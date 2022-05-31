# -*- coding: utf-8 -*-

import telebot
import requests

TOKEN = '1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0'
VK_TOKEN = '1e6fc5ae345b2af29028971a82627158b07cff065db6d25f57ed113ebf333135469fb4ff8004dc6a50da0'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите текст для установки статуса')

@bot.message_handler(content_types=["text"])
def text_message(message):
    setStatus(message.text)
    bot.reply_to(message, "Статус установлен!")

def setStatus(text):
    print('setStatus')
    requests.get('https://api.vk.com/method/status.set?access_token=' + VK_TOKEN + "&text=" + text + "&v=5.131")


bot.polling(none_stop=True)