from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.db import *

def use_handler(bot, update, msg_list):
    item = msg_list[2]
    chat_id = update.message.chat_id
    if len(msg_list) > 3:
        username = msg_list[3].replace("@","")
    else:
        username = update.message.from_user.username

    if item == "cake":
        use_message = " ate the cake and got fat. They also receive compensation of 20."
        add_money(chat_id, username, 20)
    elif item == "coke":
        use_message = " drank coke, got amazing energy, worked as a sweaper and made 40 bucks."
        add_money(chat_id, username, 40)
    elif item == "chillpill":
        use_message = " took a chill pill. They chilling."
    elif item == "apple":
        use_message = " was the one to drop his apple on newton's head, the science community gave him 80 bucks for that."
        add_money(chat_id, username, 80)

    update.message.reply_text(username + use_message)