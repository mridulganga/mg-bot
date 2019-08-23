from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.db import *

def admin_handler(bot, update, msg_list):
    chat_id = update.message.chat_id

    if bot.get_member(chat_id, update.message.from_user.id).status in ['creator', 'administrator']:
        is_admin=True

    else:
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