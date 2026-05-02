
import telebot
import os
from dotenv import load_dotenv
from telebot import types
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states import State, StatesGroup
import re

load_dotenv()

TOKEN_1 = os.getenv("TOKEN_1")

if TOKEN_1 is None:
    print("Token is not found!")
    exit()
    
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN_1, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))

class RegistrationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_phonenumber = State()

registration_kb = types.ReplyKeyboardMarkup()
registration_kb = types.KeyboardButton("Registration👍")

cancel_kb = types.InlineKeyboardMarkup()
cancel_kb.add = types.InlineKeyboardButton("Cancel🛑", callback_data="cancel")

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, 
                "Hi, enter 'Registration' to take spam on email", reply_markup=registration_kb)

@bot.message_handler(func=lambda message: message.text.startswith("Registration"))
def registration_start(message):
     
    temp_msg = bot.send_message(
    message.chat.id,
        "⏳Update interface...", reply_markup=cancel_kb)
    
    bot.delete_message(message.chat.id, temp_msg.id)
    bot.set_state(message.chat.id, temp_msg.id)
    bot.set_state(message.from_user.id, 
                RegistrationStates.waiting_for_email, 
                message.chat.id)
    
    bot.send_message(message.chat.id, 
                "Great! Send me your Email, where you want have spam.", reply_markup=cancel_kb)

@bot.message_handler(state=RegistrationStates.waiting_for_email)
def process_email(message):
    email = message.text.strip()
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    print(f"New email: {email}")

    if re.match(email_pattern, email):
        with open("emails.txt", "a") as f: 
            f.write(email + "\n")
        
        phone_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone_btn = types.KeyboardButton("Send phone", request_contact=True) 
        phone_kb.add(phone_btn)
        
        bot.set_state(message.from_user.id, RegistrationStates.waiting_for_phonenumber, message.chat.id)
        bot.send_message(message.chat.id, "Now share your phone number:", reply_markup=phone_kb)
    else:
        bot.send_message(message.chat.id, "Incorrect email. Try again.")

@bot.message_handler(state=RegistrationStates.waiting_for_phonenumber, func=lambda m: m.contact)  
def process_phone(message):
    phone = message.contact.phone_number  
    phone_pattern = r"^\+?\d{10,15}$"
    print(f"Mobile phone: {phone}")

    if re.match(phone_pattern, phone):
        with open("phones.txt", "a") as f:
            f.write(phone + "\n")
        
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Thanks! Phone saved.", reply_markup=registration_kb)
    else:
        bot.send_message(message.chat.id, "Invalid phone format. Try again.")

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_handler(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.send_message(call.message.chat.id, "Cancelled. Enter 'Registration' again.", reply_markup=registration_kb)
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()




