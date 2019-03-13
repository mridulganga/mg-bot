from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import datetime

def log_command(s):
    with open("log.txt", "a") as myfile:
        myfile.write(s)

from app.todo import todo_handler
from app.animals import animal_handler
from app.fun import fun_handler
from app.poll import poll_extras_handler
from app.monopoly import mono_handler
from app.help_strings import get_help

animal_list = ["dog","bark","bork","cat","meow","pussy","panda","redpanda",
                "pika","pikachu","fox"]
fun_list = ["google","joke", "roast", "mock", "meme", "quote", "xkcd",
                "geek", "geekjoke", "dice", "coin", "flip", "choose","select"]
monopoly_list = ["balance","daily","buy","sell","steal", "shop", "market", "store", "buy",
                "purchase", "sell", "inventory", "balance", "deposit", "withdraw",
                "lottery", "gamble", "share", "send", "steal", "rich", "beg"]

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
        help_str = "*Main Sections*:\n`Fun\nChoose\nAnimals\nTodo\nPoll\nMonopoly\n\n`*Use*:\n`pls help command`"

        bot.send_message(chat_id=update.message.chat_id, 
                text=help_str, 
                parse_mode=telegram.ParseMode.MARKDOWN)
    # update.message.reply_text('''Help is Here!
    # Fun:
    # joke, google, meme, quote, xkcd, geek, coin, dice

    # Choose:
    # pls choose item1 item2 item3

    # Animals:
    # dog, cat, panda, fox, redpanda, pika

    # Todo:
    # pls todo            -list todos
    # pls todo item       -add todo 
    # pls todo remove 2   -remove 2nd item
    # pls todo remove     -remove everything

    # Poll:
    # pls poll            -create new poll
    # pls vote 2          -vote for 2nd option
    # pls vote            -show poll votes
    # pls vote end        -end poll and show results
    # ''')


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def msg_parser(bot, update):
    msg = update.message.text.lower()
    msg_list = msg.split(" ")
    if msg_list[0] in ["mg","pls", "kini"]:
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
            #help_handler(bot,update,msg_list)
            pass
        log_command(str(update.message.chat_id) + "  || " + update.message.from_user.username + " : " + str(msg_list) + "\n")
    elif msg_list[0] in ["hello","hi"]:
        update.message.reply_text("Hello there!")
        