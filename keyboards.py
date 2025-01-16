from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES



def generate_language():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []

    for button in LANGUAGES.values():
        btn = KeyboardButton(text=button)
        buttons.append(btn)
    markup.add(*buttons)
    return markup

def generate_back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_back = KeyboardButton(text='K perevodu ↩️')
    markup.add(btn_back)
    return markup
