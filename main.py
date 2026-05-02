'''
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_1 = os.getenv("TOKEN_1")

if TOKEN_1 is None:
    print("Token is not found!")
    exit()
    
bot = telebot.TeleBot(TOKEN_1)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(type(message))
    bot.reply_to(message, "Hi, I'm Echo-Bot! Write something and I repeat it!")

@bot.message_handler(commands=["info"])
def send_info(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg_text = message.text

    print(first_name, last_name, user_id, chat_id, user_name, msg_text)
    
    reply_msg = f"Hello, {first_name}\n" \
                f"Your Telegram ID: {user_id}\n " \
                f"Your message: {msg_text} \n"

    bot.reply_to(message, reply_msg)
#   bot.send_message(37, reply_msg)

@bot.message_handler(func=lambda message: message.text.startswith("Hello"))
def hello_answer(message):
    bot.send_message(message.chat.id, "hi!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
      bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
        print("Bot is running...")
        bot.infinity_polling()

'''





