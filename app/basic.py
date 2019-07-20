from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import datetime


# def log_command(s):
#     with open("log.txt", "a") as myfile:
#         myfile.write(s)

from app.logger import msg_logger, debug_logger
from app.todo import todo_handler
from app.animals import animal_handler
from app.fun import fun_handler
from app.poll import poll_extras_handler
from app.monopoly import mono_handler
from app.help_strings import get_help
from app.news import news_handler
# import logging

animal_list = ["dog","bark","bork","cat","meow","pussy","panda","redpanda",
                "pika","pikachu","fox"]

fun_list = ["google","joke", "roast", "mock", "meme", "quote", "xkcd", "avatar", 
                "geek", "geekjoke", "dice", "coin", "flip", "choose","select",
                "unsplash", "wall", "wallpaper","die", "kill", "wink", "asktrump"]

monopoly_list = ["balance", "beg", "daily", "search", "buy", "sell", "use", "steal", "shop", "market", "store", 
                "purchase", "inventory", "deposit", "withdraw",
                "lottery", "gamble", "share", "send", "rich", "loan"]

news_list = ["news", "entertainment", "general", "health", "science", "sports", "technology"]

def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update, msg_list):
    if len(msg_list) > 2:
        help_str = get_help(msg_list[2])
        # update.message.reply_text("Help : \n" + help_str)
        bot.send_message(chat_id=update.message.chat_id, 
                text=help_str, 
                parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        help_str = "*Main Sections*:\n`Fun\nChoose\nAnimals\nTodo\nPoll\nMonopoly\nNews\n\n`*Use*:\n`pls help command`"

        bot.send_message(chat_id=update.message.chat_id, 
                text=help_str, 
                parse_mode=telegram.ParseMode.MARKDOWN)

def error(bot, update, msg_list):
    debug_logger.debug(str(update.message.chat_id) + " - " + update.message.from_user.username + " || " + str(msg_list))


def msg_parser(bot, update):
    msg = update.message.text.lower()
    msg_list = msg.split(" ")
    if msg_list[0] in ["mg","pls", "kini"]:

        if len(msg_list) == 1:
            return

        if msg_list[1] in animal_list:
            animal_handler(bot, update, msg_list)

        elif msg_list[1] in ["games","game"]:
            pass

        elif msg_list[1] in monopoly_list:
            mono_handler(bot,update,msg_list)

        elif msg_list[1] in ["images", "image", "pics", "pic", "photos", "photo"]:
            pass 

        elif msg_list[1] in fun_list:
            fun_handler(bot,update, msg_list)

        elif msg_list[1] in news_list:
            news_handler(bot, update, msg_list)

        elif msg_list[1] in ["do","todo","tasks"]:      #done
            todo_handler(bot, update, msg_list[1:])

        elif msg_list[1] in ["calender","cal", "events", "event"]:
            pass

        elif msg_list[1] in ["now", "time"]:
            update.message.reply_text(str(datetime.datetime.utcnow()))

        elif msg_list[1] in ["vote","poll"]:
            poll_extras_handler(bot, update, msg_list)

        elif msg_list[1] == "help":
            help(bot,update,msg_list)
        else:
            debug_logger.debug(str(msg_list))
            #help(bot,update,msg_list)

        msg_logger.info(str(update.message.chat_id) + "  || " + update.message.from_user.username + " : " + str(msg_list))
    elif msg_list[0] in ["hello","hi"]:
        update.message.reply_text("Hello there!")
        
