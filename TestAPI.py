import telebot
from telebot import types
from TelegramEasy.Bot_token import test_Token, PSWS
from Currency.Curency_def import currency_check_usd, currency_check_eur
from google_sheets.do_cargo_google import do_cargo_google
import sqlite3

bot = telebot.TeleBot(test_Token)
USERS = {}

class User:
    def __init__(self, company):
        self.company = company
        self.name = None
        self.psw = None


@bot.message_handler(commands=['start']) # Процесс регистрации участника
def do_start(message):
    try:
        user = message.from_user.first_name
        user_id = message.from_user.id

        con = sqlite3.connect('/Users/rob/Documents/Code/my_projects/TelegramEasy/dbtelega.db')
        cur = con.cursor()
        cur.execute('SELECT user_id FROM users')
        data = cur.fetchall()
        new_data = []
        for el in data:
            new_data.append(el[0])
        cur.close()
        con.close()

        if user_id in new_data:
            bot.reply_to(message, f'{user}! Вы уже зарегистрированны в системе. Выполнение данной команды повторно невозможно!')

        else:
            if user:
                name = user
            else:
                name = 'Аноним'
            bot.reply_to(message, f'Привет, {name}! \n'
                          f'Рады приветствовать Вас в EasyBot - Вашем личном помощнике при работе с компанией EasyВЭД\n'
                          f'Прошу вас пройти быструю регистрацию для корректной работы бота!')

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('Зитрек')
            itembtn2 = types.KeyboardButton('Инспорт')
            itembtn3 = types.KeyboardButton('ДАК')
            itembtn4 = types.KeyboardButton('Экономка')
            itembtn5 = types.KeyboardButton('Дементра')
            itembtn6 = types.KeyboardButton('Эколайн')
            itembtn7 = types.KeyboardButton('Шмидт')
            itembtn8 = types.KeyboardButton('EasyВЭД')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8)

            msg = bot.send_message(message.chat.id, 'Какую компанию вы представляете?', reply_markup=markup)
            bot.register_next_step_handler(msg, process_company_step)
    except Exception as e:
        bot.reply_to(message,f'{message.from_user.first_name}, сервис временное не доступен! Прошу обратиться к администратору!')

def process_company_step(message):
    user_id = message.from_user.id
    USERS[user_id] = User(message.text)

    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(user_id, 'Введите пароль для продолжения работы:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_psw_step)


def process_psw_step(message):
    user_id = message.from_user.id
    user = USERS[user_id]
    try:
        if PSWS[user.company] == message.text:

            user.psw = message.text

            msg = bot.send_message(user_id, 'Как Вас зовут?')
            bot.register_next_step_handler(msg, process_name_step)

        else:
            bot.reply_to(message, 'Вы ввели неправильный пароль! Попробуйте еще раз.')

    except Exception as e:
        bot.reply_to(message, 'Вы ввели неправильный пароль! Попробуйте еще раз.')

def process_name_step(message):
    user_id = message.from_user.id
    user = USERS[user_id]
    user.name = message.text

    bot.send_message(user_id, f'{user.name}, спасибо Вам за ответы! \n'
                              f'Вы зарегистрированы как представитель компании {user.company}')

    con = sqlite3.connect('/Users/rob/Documents/Code/my_projects/TelegramEasy/dbtelega.db')
    cur = con.cursor()
    cur. execute(f'INSERT INTO users VALUES({user_id}, "{user.name}", "{user.company}", "{user.psw}")')
    con.commit()
    cur.close()
    con.close()


def check_company_Easy(message):
    bot.reply_to(message, f'{message.from_user.first_name}, актуальный статус по грузам {message.text}\n'
                          f'{do_cargo_google(message.text)}')


@bot.message_handler(commands=['help'])
def do_help(message):
    try:
        user_id = message.from_user.id
        con = sqlite3.connect('/Users/rob/Documents/Code/my_projects/TelegramEasy/dbtelega.db')
        cur = con.cursor()
        cur.execute('SELECT user_id FROM users')
        data = cur.fetchall()
        new_data = []
        for el in data:
            new_data.append(el[0])
        cur.close()
        con.close()

        if user_id in new_data:
            bot.reply_to(message, f'{message.from_user.first_name}, Вы уже прошли регистрацию!\n'
                          f'Вы можете использовать следующие команды:'
                          f'\n/usd или /eur – для получения актуального биржевого курса нужной вам валюты'
                          f'\n/cargo – для получения полной информации по всем вашим грузам в пути')
        else:
            bot.reply_to(message, f'{message.from_user.first_name}, просим Вас пройти регистрацию /start\n'
                                  f'Без регистрации Вы можете воспользоваться следующими командами: \n'
                                  f'/usd и /eur для получения актуальных курсов валют\n'
                                  f'Для получения всех возможностей бота необходимо пройти регистрацию /start')
    except Exception as e:
        bot.reply_to(message, f'Просим Вас пройти регистрацию /start\n'
                              f'Без регистрации Вы можете воспользоваться следующими командами: \n'
                              f'/usd и /eur для получения актуальных курсов валют\n'
                              f'Для получения всех возможностей бота необходимо пройти регистрацию /start')

@bot.message_handler(commands=['usd'])
def do_usd(message):
    bot.reply_to(message, f'{message.from_user.first_name}\n'
                          f'{currency_check_usd()}')

@bot.message_handler(commands=['eur'])
def do_eur(message):
    bot.reply_to(message, f'{message.from_user.first_name}\n'
                          f'{currency_check_eur()}')


@bot.message_handler(commands=['cargo'])
def do_cargo(message):
    try:
        user_id = message.from_user.id
        con = sqlite3.connect('/Users/rob/Documents/Code/my_projects/TelegramEasy/dbtelega.db')
        cur = con.cursor()
        cur.execute('SELECT user_id FROM users')
        data = cur.fetchall()
        new_data = []
        for el in data:
            new_data.append(el[0])

        if user_id in new_data:
            comp = cur.execute(f'SELECT company FROM users WHERE user_id = {user_id}')
            for el in comp:
                comp_name = el[0]

            if comp_name != 'EasyВЭД':
                bot.reply_to(message, f'{message.from_user.first_name}, актуальный статус по грузам {comp_name}\n'
                              f'{do_cargo_google(comp_name)}')
            elif comp_name == 'EasyВЭД':
                msg = bot.reply_to(message, 'Какую компанию проверяем?')
                bot.register_next_step_handler(msg, check_company_Easy)

        else:
            bot.reply_to(message, 'Для выполнения данной команды Вам необходимо пройти регистрацию /start')

        cur.close()
        con.close()
    except Exception as e:
        bot.reply_to(message, 'Для выполнения данной команды Вам необходимо пройти регистрацию /start')

@bot.message_handler(content_types=['text'])
def echo_all(message):
    if 'помощь' in message.text:
        bot.reply_to(message, 'Возможно Вам сможет помочь команда /help')
        return
    elif 'курс' in message.text:
        bot.reply_to(message, 'Курс какой валюты вам нужен? \n/usd  \n/eur')
        return
    bot.reply_to(message, 'Попробуйте начать с команды /help')


bot.polling()




