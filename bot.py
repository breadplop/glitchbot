from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from load_data import get_indv_menus, load_data
import datetime as dt

import pymongo
from pprint import pprint

bot = TeleBot(environ['TELEGRAM_TOKEN'])
bf_menu, dinz_menu = load_data()

text_messages = {
    'welcome':
        u'Hello there! I am your new Eusoff Meal Bot.\n'
        u'\nTo share: https://t.me/eusoff_bot',

    'info':
        u'Hello there!\n'
        u'I am a bot that will provide the breakfast and dinner menus of Eusoff\n'
        u'\nCommands\n'
        u'/start - start up the Eusoff bot\n'
        u'/info - more info about the bot and commands\n'
        u'/feedback - give us feedback on the bot (and request for features!)\n',

    'feedback':
        u'Feel free to leave down any suggestions/opinions at https://goo.gl/forms/zaOOUhiJhH8RzlZx2\n'
        u'We appreciate all kinds of feedback!'
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, text_messages['welcome'])
    bot.send_message(message.chat.id, "Hungry? Let's get started!", reply_markup=gen_markup())


@bot.message_handler(commands=['info'])
def on_info(message):
    bot.reply_to(message, text_messages['info'])


@bot.message_handler(commands=['feedback'])
def on_feedback(message):
    bot.reply_to(message, text_messages['feedback'])


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("MENU", callback_data="get_menu"))
    return markup


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Tdy's Bf 🍞", callback_data="cb_tdy_bf"),
               InlineKeyboardButton("Tdy's Dinz 🍱", callback_data="cb_tdy_din"),
               InlineKeyboardButton("Tmr's Bf 🍞", callback_data="cb_tmr_bf"),
               InlineKeyboardButton("Tmr's Dinz 🍱", callback_data="cb_tmr_din"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    date = dt.datetime.fromtimestamp(call.message.date)
    entry = {
        'date': date,
        'button': call.data,
        'username': call.message.chat.username,
        'type': 'callbackquery'
    }
    print(call)
    if call.data != 'get_menu':
        db_collection.insert_one(entry)

    if call.data == "get_menu":
        bot.send_message(call.message.chat.id, 'Select one:', parse_mode='Markdown', reply_markup=gen_markup())
    if call.data == "cb_tdy_bf":
        # menu=tdy_bf_m
        menu = get_indv_menus('Breakfast', date)
        bot.send_message(call.message.chat.id, menu, parse_mode='Markdown', reply_markup=menu_markup())
    if call.data == "cb_tdy_din":
        # menu=tdy_din_m
        menu = get_indv_menus('Dinner', date)
        bot.send_message(call.message.chat.id, menu, parse_mode='Markdown', reply_markup=menu_markup())
    elif call.data == "cb_tmr_bf":
        # menu=tmr_bf_m
        menu = get_indv_menus('Breakfast', date + dt.timedelta(days=1))
        bot.send_message(call.message.chat.id, menu, parse_mode='Markdown', reply_markup=menu_markup())
    elif call.data == "cb_tmr_din":
        # menu=tdy_din_m
        menu = get_indv_menus('Dinner', date + dt.timedelta(days=1))
        bot.send_message(call.message.chat.id, menu, parse_mode='Markdown', reply_markup=menu_markup())


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Hungz???", reply_markup=gen_markup())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, I do not understand. Try /start /help /info")


def listener(messages):
    for m in messages:
        print(str(m))
        log = {
          'date': dt.datetime.fromtimestamp(m.date),
          'text': m.json['text'],
          'username': m.json['from']['username'],
          'type': 'message'
        }
        db_collection.insert_one(log)
        print('inserted to mongo db')


user = environ['MONGO_USERNAME']
password = environ['MONGO_PASSWORD']
database = environ['MONGO_DB_NAME']
connection_end = 'cluster0-shard-00-00-dbct0.mongodb.net:27017,cluster0-shard-00-01-dbct0.mongodb.net:27017,cluster0-shard-00-02-dbct0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'

client = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format(user, password, connection_end))
db = client[database]
# change this to start another collection
db_collection = db.testing
pprint(client.list_database_names())

bot.set_update_listener(listener)
bot.set_webhook("https://{0}.glitch.me/{1}".format(environ['PROJECT_NAME'], environ['TELEGRAM_TOKEN']))
