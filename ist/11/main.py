from datetime import datetime, timedelta
import xml.dom.minidom
import requests
import telebot
from telebot import types
from enum import Enum

class ChatState(Enum):
    INITIAL = 0
    VALUTE_INPUT = 1


TOKEN = '1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0'

bot = telebot.TeleBot(TOKEN)

chat_state = ChatState.INITIAL

valute_code = ""

@bot.message_handler(commands=['start'])
def send_valute_keyboard(message):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*[types.InlineKeyboardButton(text="Доллары США", callback_data="R01235"), 
                   types.InlineKeyboardButton(text="Евро", callback_data="R01239")])

    bot.send_message(message.chat.id, "Выберите валюту", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda update: update.data)
def send_new_state(update):
    global chat_state
    global valute_code

    chat_state = ChatState.VALUTE_INPUT
    valute_code = update.data
    bot.send_message(update.message.chat.id, "Выберите дату в формате dd/mm/yy")

@bot.message_handler(content_types=['text'])
def date_input(message):
    global chat_state
    global valute_code

    if chat_state == ChatState.VALUTE_INPUT:
        
        try:
            date = datetime.strptime(message.text, "%d/%m/%y")
            
            result = ""
            print(message.text)
            day = str(date.day)
            month = str(date.month)

            if (len(day) == 1):
                day = '0' + day

            if (len(month) == 1):
                month = '0' + month

            date_query = day + "/" + month + "/" + str(date.year)
            print(date_query)
            response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date_query)
            print(response.text)
            dom = xml.dom.minidom.parseString(response.text)

            valutes = dom.getElementsByTagName("Valute")

            for valute in valutes:
                if valute.getAttribute("ID") == valute_code:
                    new_value = float(valute.getElementsByTagName("Value")[0].childNodes[0].nodeValue.replace(',','.'))
                    result = result + "Курс за " + date_query + ": " + str(new_value) + "\n"


            bot.send_message(message.chat.id, result)

            chat_state = ChatState.INITIAL
            valute_code = ""
            send_valute_keyboard(message)
        except ValueError as e:
            print(str(e))
            bot.send_message(message.chat.id, "Дата указано некорректно. Правильный формат: dd/mm/yyyy")


bot.infinity_polling()