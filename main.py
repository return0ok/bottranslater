from telebot import TeleBot
from telebot.types import Message
from configs import *
from keyboards import *
import sqlite3
from googletrans import Translator


bot = TeleBot(TOKEN, parse_mode='HTML')

@bot.message_handler(commands = ['start', 'help', 'about_dev', 'history'])
def start (message: Message):
    full_name = message.from_user.full_name
    chat_id = message.chat.id
    # print(full_name)
    if message.text == '/start':
        bot.send_message(chat_id, f'''Privet {full_name}. Ya bot perevodchik. Ya pomogu''')
        # bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEMJmVmSwVFx7ouhDX8CC9sB5tFwgr_EgACpgADWngGAAG_0nY2M2rHMDUE')
        start_translate(message)
    elif message.text == '/help':
        bot.send_message(chat_id, f'''Privet {full_name}. Eta bot razrabativalsya dlya uchebnix seley!''', reply_markup=generate_back())
        # bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEMJmdmSwWvQmguc6iaCpEX9xedX9gfXQACWgADYIltDDFctP-jY4ofNQQ')
    elif message.text == '/about_dev':
        bot.send_message(chat_id, f'''Privet {full_name}. Eta bot razrabotivalsya razrabotchikom
         t.me/jiefbeewfbew''', reply_markup=generate_back())
    elif message.text == '/history':
        return_history(message)

def return_history(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Eto vashi poslednie 10 perevodinie teksti: ')

    database = sqlite3.connect('tranlater.db')
    cursor = database.cursor()

    cursor.execute('''
        select from_lang, to_lang, original_text, tranlated_text from history
        where telegram_id = ?
    ''', (chat_id, ))
    history = cursor.fetchall()
    # print(history)
    history = history[::-1]
    # print(history)
    r = 0
    for from_lang, to_lang, org_text, tr_text in history[:10]:
        r += 1
        bot.send_message(chat_id, f''' {r}. <i>Vi perevodili:</i>
        <b>S yazika:</b> {from_lang}
        <b>Na yazik:</b> {to_lang}
        <b>Tekst:</b> {org_text}
        <b>Bot perevel:</b> {tr_text} ''')

@bot.message_handler(commands=['/pay'])
def command_pay(message):
    chat_id = message.chat.id

    bot.send_invoice(
        provider_token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'

    )

@bot.message_handler(func=lambda message: "K perevodu ↩️" in message.text)
def back_translate(message):
    start_translate(message)

def start_translate(message: Message):
    chat_id = message.chat.id

    msg = bot.send_message(chat_id, f'Viberite s kakogo yazika xotite perevesti ?',
                     reply_markup=generate_language())
    bot.register_next_step_handler(msg, second_language)


def second_language(message: Message):
    if message.text in ['/start', '/help', '/about_dev', '/history']:
        start(message)
    else:
        chat_id = message.chat.id
        src = message.text
        msg = bot.send_message(chat_id, f'Viberita na kakaoy yazik xotite perevesti dlya testov?',
                         reply_markup=generate_language())
        bot.register_next_step_handler(msg, give_me_text, src)


def give_me_text(message: Message, src):
    if message.text in ['/start', '/help', '/about_dev', '/history']:
        start(message)
    else:
        chat_id = message.chat.id
        dest = message.text
        msg = bot.send_message(chat_id, 'Napishite teks ili slova ili dlya testov chtota?')
        bot.register_next_step_handler(msg, translate, src, dest)


def translate(message: Message, src, dest):
    if message.text in ['/start', '/help', '/about_dev', '/history']:
        start(message)
    else:
        chat_id = message.chat.id
        text = message.text
        translator = Translator()
        tr_text = translator.translate(text=text, src=get_key(src), dest = get_key(dest))
        bot.send_message(chat_id, tr_text.text)

        database = sqlite3.connect('tranlater.db')
        cursor = database.cursor()

        cursor.execute('''
            INSERT INTO history (telegram_id, from_lang, to_lang, original_text, tranlated_text)
            VALUES (?,?,?,?,?) 
        ''', (chat_id, src, dest, text, tr_text.text))
        database.commit()
        database.close()

        start_translate(message)




# bot.polling(none_stop=True)
bot.infinity_polling()