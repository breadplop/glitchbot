from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from load_data import load_data, format_menu, get_all_menus

bot = TeleBot(environ['TELEGRAM_TOKEN'])
bf_menu, dinz_menu = load_data()

text_messages = {
    'welcome':
        u'Hello there! I am your new Eusoff Meal Bot.'
        u'To start, enter "I love Eusoff"',

    'info':
        u'Hello there!\n'
        u'I am a bot that will provide the breakfast and dinner menus of Eusoff\n',

    'wrong_chat':
        u'Hi there!\nThanks for trying me out!\n'
        u'We hope you find this useful. \n For any feedback/comments, please message @... \n'
        u'https://t.me/breadtest_bot'
}

#bf_menu_tdy = format_menu(bf_menu[tdy])
tdy_bf_m, tdy_din_m, tmr_bf_m, tmr_din_m = get_all_menus()
GROUP_CHAT_ID = int(environ["GROUP_CHAT_ID"])

def is_api_group(chat_id):
    return chat_id == GROUP_CHAT_ID
  
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.reply_to(message, "Hello " + message.first_name + text_messages['welcome'])
  bot.reply_to(message, text_messages['welcome'])
    
@bot.message_handler(commands=['info'])
def on_info(message):
  if not is_api_group(message.chat.id):
      bot.reply_to(message, text_messages['wrong_chat'])
      return 

  bot.reply_to(message, text_messages['info'])
    
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
  print("does it come here? ", call)
  if call.data == "cb_tdy_bf":
    bot.send_message(call.message.chat.id, tdy_bf_m, parse_mode='Markdown',reply_markup=gen_markup())
  if call.data == "cb_tdy_din": 
    bot.send_message(call.message.chat.id, tdy_din_m, parse_mode='Markdown',reply_markup=gen_markup())
  elif call.data == "cb_tmr_bf":
    bot.send_message(call.message.chat.id, tmr_bf_m, parse_mode='Markdown',reply_markup=gen_markup())
    #bot.answer_callback_query(call.id, text = "tmr bf")
  elif call.data == "cb_tmr_din":
    bot.send_message(call.message.chat.id, tmr_din_m, parse_mode='Markdown',reply_markup=gen_markup())
    #bot.answer_callback_query(call.id, text = "today's dinner")

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