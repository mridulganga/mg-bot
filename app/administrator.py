from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.db import *

def admin_handler(bot, update, msg_list):
    chat_id = update.message.chat_id
    
    if_admin=False
    for admin in bot.get_chat_administrators(chat_id):
        if admin.user.username == update.message.from_user.username:
            if_admin = True

    if is_admin==False:
        update.message.reply_text("You are not admin.")
        return
    
    if len(msg_list) > 2:
        
        # clear loan
        # pls admin loan clear @mridul
        if msg_list[2] == "loan":

            user = msg_list[4].replace("@","")
            clear_loan(chat_id, user)
            update.message.reply_text("Loan has been cleared for " + user)

        # ban user
        # pls admin ban @mridul
        if msg_list[2] == "ban":
            user = msg_list[3].replace("@","")