import telebot
import os
import random
from telebot import types
from dotenv import load_dotenv

load_dotenv()
TOKEN_3 = os.getenv("TOKEN_3")
bot = telebot.TeleBot(TOKEN_3)

if TOKEN_3 is None:
    print("Token is not found!")
    exit()

games = {}


@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, 
                "Hi, I'm Tic-Tac-Toe Bot. Let's play.")

    games[user_id] = {
        "board": [" "] * 9,
        "player": "",
        "bot": ""
    }

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❌", callback_data="X"), types.InlineKeyboardButton("⭕", callback_data="O"))

    bot.send_message(message.chat.id, "Choose X or O:", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data in ("X", "O"))
def choose_symbol(call):
    user_id = call.from_user.id
    game = games[user_id]
    game["player"] = call.data


    if call.data == "X":
        game["bot"] = "O"
    else:
        game["bot"] = "X"

    keyboard = create_board(game["board"])

    bot.edit_message_text(
        "Game started!",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard)

def create_board(board):

    markup = types.InlineKeyboardMarkup(row_width=3)

    buttons = []

    for i in range(9):
        text = board[i]
        if text == " ":
            text = "⬜"

        button = types.InlineKeyboardButton(
            text,
            callback_data=f"move_{i}"
        )

        buttons.append(button)
    markup.add(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("move"))
def move(call):

    user_id = call.from_user.id
    game = games[user_id]
    board = game["board"]
    index = int(call.data.split("_")[1])



    if board[index] != " ":
        return


    board[index] = game["player"]
    winner = check_winner(board)

    if winner:
        finish_game(call, winner)
        return


    empty = []
    for i in range(9):
        if board[i] == " ":
            empty.append(i)

    if len(empty) > 0:

        bot_move = random.choice(empty)
        board[bot_move] = game["bot"]


    winner = check_winner(board)

    if winner:
        finish_game(call, winner)
        return


    keyboard = create_board(board)

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )


def check_winner(board):

    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],

        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],

        [0, 4, 8],
        [2, 4, 6]
    ]

    for line in wins:

        a = line[0]
        b = line[1]
        c = line[2]

        if board[a] == board[b] == board[c]:

            if board[a] != " ":
                return board[a]


    if " " not in board:
        return "draw"

    return None


def finish_game(call, winner):

    user_id = call.from_user.id

    game = games[user_id]

    if winner == "draw":
        text = "Draw"

    elif winner == game["player"]:
        text = "You win"

    else:
        text = "I win"

    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id
    )

    del games[user_id]


if __name__ == "__main__":
    print("Bot is running...")

bot.infinity_polling()