from app.db import *
from app.logger import logger

def admin_handler(bot, update, msg_list):
    chat_id = update.message.chat_id
    logger.debug("Reached handler")
    if bot.get_member(chat_id, update.message.from_user.id).status in ['creator', 'administrator']:
        is_admin=True
        logger.debug("User is admin")
    else:
        update.message.reply_text("You are not admin.")
        logger.debug("User not admin")
        return
    
    if len(msg_list) > 2:
        
        # clear loan
        # pls admin loan clear @mridul
        if msg_list[2] == "loan":
            logger.debug("clearing loan")
            user = msg_list[4].replace("@","")
            clear_loan(chat_id, user)
            update.message.reply_text("Loan has been cleared for " + user)

        # ban user
        # pls admin ban @mridul
        if msg_list[2] == "ban":
            user = msg_list[3].replace("@","")