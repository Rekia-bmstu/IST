import telebot
from telebot import types

bot = telebot.TeleBot("1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0")


class Button:
    def __init__(self, btnName, reactionText, reactionKeyboard):
        self.btnName = btnName
        self.reactionText = reactionText
        self.reactionKeyboard = reactionKeyboard
        self.clicks = 0

DEFAULT_BUTTONS = [Button("Натуралы", "Нормальный ты тип", ["C#", "KOTLIN"]),
                   Button("Геи", "Why are you gay???", ["JS", "PYTHON"])]

BUTTONS = [Button("C#", "Топ язык для бека", DEFAULT_BUTTONS),
           Button("KOTLIN", "Нормальный мобильный разраб", DEFAULT_BUTTONS),
           Button("JS", "Для фронтендеров...", DEFAULT_BUTTONS)]


@bot.message_handler(commands=['start'])
def start(message):
    sendKeyboard(message.chat.id, "Выбери тип", DEFAULT_BUTTONS)

@bot.message_handler(content_types=["text"])
def reply_message(message):
    btn = list(filter(lambda btn: btn.btnName == message.text, DEFAULT_BUTTONS + BUTTONS))[0]
    btn.clicks += 1
    sendKeyboard(message.chat.id, btn.reactionText + "\n" + "Нажатий: " + str(btn.clicks), btn.reactionKeyboard)

def sendKeyboard(chatId, message, keyButtons):
    keyboard = types.ReplyKeyboardMarkup()

    for keyButton in keyButtons:
        keyboard.add(types.KeyboardButton(keyButton))

    bot.send_message(chatId, message, reply_markup=keyboard)

bot.polling(none_stop=True)
