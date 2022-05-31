import telebot
from functools import reduce
from telebot import types

bot = telebot.TeleBot("1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0")


class Button:
    def __init__(self, btnName, reactionText, reactionKeyboard):
        self.btnName = btnName
        self.reactionText = reactionText
        self.reactionKeyboard = reactionKeyboard
        self.clicks = 0

def buttons_to_btn_names_list(buttons):
    return [btn.btnName for btn in buttons]
    
DEFAULT_BUTTONS = [Button("Backend", "Нормальный ты тип", ["C#", "GO", "Обнулить C#", "Обнулить GO"]),
                   Button("Frontend", "Why are you gay???", ["JS", "TS", "Обнулить JS", "Обнулить TS"]),
                   Button("Результаты", "", ["JS", "TS", "Обнулить JS", "Обнулить TS"])]

BUTTONS = [Button("C#", "Топ язык для бека", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("GO", "Фанат микросервисов??", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("JS", "Для фронтендеров...", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("TS", "Для фронтендеров...", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("Обнулить C#", "Обнулил", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("Обнулить GO", "Обнулил", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("Обнулить JS", "Обнулил", buttons_to_btn_names_list(DEFAULT_BUTTONS)),
           Button("Обнулить TS", "Обнулил", buttons_to_btn_names_list(DEFAULT_BUTTONS))]

ALL_BUTTONS = DEFAULT_BUTTONS + BUTTONS

@bot.message_handler(commands=['start'])
def start(message):
    sendKeyboard(message.chat.id, "Выбери тип", list(map(lambda btn: btn.btnName, DEFAULT_BUTTONS)))

@bot.message_handler(content_types=["text"])
def reply_message(message):
    pressedButton = list(filter(lambda btn: btn.btnName == message.text, DEFAULT_BUTTONS + BUTTONS))[0]
    pressedButton.clicks += 1

    if 'Обнулить' in pressedButton.btnName and pressedButton.btnName != 'Backend' and pressedButton.btnName != 'Frontend':
        excludedDropButtons = list(filter(lambda btn: 'Обнулить' not in btn.btnName, ALL_BUTTONS))
        print([btn.btnName for btn in excludedDropButtons])
        buttonToDrop = list(filter(lambda btn: btn.btnName in message.text, excludedDropButtons))[0]
        buttonToDrop.clicks = 0
        bot.send_message(message.chat.id, f"Нажатий у {buttonToDrop.btnName}: {buttonToDrop.clicks}")
        sendKeyboard(message.chat.id, "Выбери тип", list(map(lambda btn: btn.btnName, DEFAULT_BUTTONS)))
    elif pressedButton.btnName == "Результаты":
        excludedDropButtons = list(filter(lambda btn: 'Обнулить' not in btn.btnName, BUTTONS))
        clicks_for_btn = [f"{btn.btnName}: {btn.clicks}\n" for btn in excludedDropButtons]
        msg = reduce(lambda acc, next: acc + next, clicks_for_btn)
        bot.send_message(message.chat.id, msg)
        sendKeyboard(message.chat.id, "Выбери тип", list(map(lambda btn: btn.btnName, DEFAULT_BUTTONS)))
    else:
        sendKeyboard(message.chat.id, pressedButton.reactionText + "\n" + "Нажатий: " + str(pressedButton.clicks), pressedButton.reactionKeyboard)


def sendKeyboard(chatId, message, keyButtons):
    keyboard = types.ReplyKeyboardMarkup()

    for keyButton in keyButtons:
        keyboard.add(types.KeyboardButton(keyButton))

    bot.send_message(chatId, message, reply_markup=keyboard)

def show_results():
    pass

bot.polling(none_stop=True)
