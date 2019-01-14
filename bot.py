from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from load_data import load_data, format_menu, get_indv_menus, format_date
import datetime as dt

bot = TeleBot(environ['TELEGRAM_TOKEN'])
bf_menu, dinz_menu = load_data()

text_messages = {
    'welcome':
        u'Hello there! I am your new Eusoff Meal Bot.'
        u' This is a test',

    'info':
        u'Hello there!\n'
        u'I am a bot that will provide the breakfast and dinner menus of Eusoff\n',

    'wrong_chat':
        u'Hi there!\nThanks for trying me out!\n'
        u'We hope you find this useful. \n For any feedback/comments, please message @... \n'
        u'https://t.me/breadtest_bot',
      'feedback':
        u'Feel free to leave down any suggestions/opinions at https://goo.gl/forms/zaOOUhiJhH8RzlZx2 \n'
        u'We appreciate all kinds of feedback!'
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.reply_to(message, "Hello " + message.first_name + text_messages['welcome'])
  bot.reply_to(message, text_messages['welcome'])
    
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
  markup.add(InlineKeyboardButton("Tdy's Bf 🍞", callback_data="cb_tdy_bf"), \
             InlineKeyboardButton("Tdy's Dinz 🍱", callback_data="cb_tdy_din"), \
             InlineKeyboardButton("Tmr's Bf 🍞", callback_data="cb_tmr_bf"), \
             InlineKeyboardButton("Tmr's Dinz 🍱", callback_data="cb_tmr_din"))
  return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  #bot.answer_callback_query(call.id, {text:"Answer is No"})
  #get_indv_menus(bf_menu,format_date(tdy_raw))
  #menu = get_indv_menus(bf_menu,format_date(message.date))
  #print("does it come here? ", call)
  date = dt.datetime.fromtimestamp(call.message.date)
  if call.data=="get_menu":
    bot.send_message(call.message.chat.id, 'Select one:', parse_mode='Markdown',reply_markup=gen_markup())
  if call.data == "cb_tdy_bf":
    #menu=tdy_bf_m
    menu = get_indv_menus('Breakfast', date)
    bot.send_message(call.message.chat.id, menu, parse_mode='Markdown',reply_markup=menu_markup())
  if call.data == "cb_tdy_din": 
    #menu=tdy_din_m
    menu = get_indv_menus('Dinner', date)
    bot.send_message(call.message.chat.id, menu, parse_mode='Markdown',reply_markup=menu_markup())
  elif call.data == "cb_tmr_bf":
    #menu=tmr_bf_m
    menu = get_indv_menus('Breakfast', date + dt.timedelta(days=1))
    bot.send_message(call.message.chat.id, menu, parse_mode='Markdown',reply_markup=menu_markup())
  elif call.data == "cb_tmr_din":
    #menu=tdy_din_m
    menu = get_indv_menus('Dinner', date + dt.timedelta(days=1))
    bot.send_message(call.message.chat.id, menu, parse_mode='Markdown',reply_markup=menu_markup())

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Hungz???", reply_markup=gen_markup())

  
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, "Sorry, I do not understand. Try /start /help /info")

def listener(messages):
    for m in messages:
        print(str(m))


bot.set_update_listener(listener)

bot.set_webhook("https://{}.glitch.me/{}".format(environ['PROJECT_NAME'], environ['TELEGRAM_TOKEN']))