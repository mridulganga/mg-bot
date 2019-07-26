import telegram

from app.db import get_help

def help_handler(bot, update, msg_list):
    if len(msg_list) > 2:
        help_obj = get_help(msg_list[2])
        help_str = "*" + help_obj["title"] + "*\n" + help_obj["description"].encode("utf-8").decode("unicode_escape")
        
        bot.send_message(chat_id=update.message.chat_id, 
                text=help_str, 
                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        help_obj = get_help("*")
        help_str = "*" + help_obj["title"] + "*\n" + help_obj["description"].encode("utf-8").decode("unicode_escape")
        bot.send_message(chat_id=update.message.chat_id, 
                text=help_str, 
                parse_mode=telegram.ParseMode.MARKDOWN)