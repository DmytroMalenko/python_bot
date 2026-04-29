import telebot
import os
import string
import random
from telebot import types
from dotenv import load_dotenv

# Task 1
'''
load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("Token is not found!")
    exit()
    
bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def ask(message):
    ask1 = ["Do you like coffee?", "Have you ever traveled abroad?", "Can you swim?", \
"Do you work?", \
"Is it raining right now?", \
"Do you enjoy reading books?", \
"Have you finished your homework?",\
"Do you speak more than one language?",\
"Are you feeling tired today?",\
"Do you use social media every day?"]
    answer = ["Yes.", "No."]
    if message.text in ask1:
        bot.send_message(message.chat.id, random.choice(answer))

bot.infinity_polling()



# Task 2

load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("Token is not found!")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def info(message):

    str = string.ascii_letters + string.digits + string.punctuation
    passw = "".join(random.choice(str) for _ in range(int(message.text)))
    bot.reply_to(message, "Hi, here is your safety password:")
    bot.send_message(message.chat.id, passw)

bot.infinity_polling()

'''
# Task 3

load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("Token is not found!")
    exit()
    
bot = telebot.TeleBot(TOKEN)

def board():
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Stone",  callback_data="stone")
    item2 = types.InlineKeyboardButton("Shears",  callback_data="shears")
    item3 = types.InlineKeyboardButton("Papier",  callback_data="papier")

    markup.add(item1, item2, item3)
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi, choose stone, shears or papier.", reply_markup=board())

@bot.callback_query_handler(func=lambda call: True)

def play(call):
    bot_choice = random.choice(["Stone", "Shears", "papier"])
    if call.data == bot_choice:
        bot.send_message(call.message.chat.id, f"Draw, your choice: {call.data}\n My choise was: {bot_choice}")

    elif (call.data == "stone" and bot_choice == "shears") or \
         (call.data == "shears" and bot_choice == "papier") or \
         (call.data == "papier" and bot_choice == "stone"): 
        bot.send_message(call.message.chat.id, f"You win, your choice: {call.data}\n My choise was: {bot_choice}") 
    else: 
        bot.send_message(call.message.chat.id, f"I win, your choice: {call.data}\n My choise was: {bot_choice}")
    reply_markup=board()

bot.infinity_polling()