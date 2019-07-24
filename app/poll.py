from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from app.db import create_poll, end_poll, vote_poll, get_votes, get_poll_options


pobj = {}

def pollbegin(bot, update):
    global pobj
    pobj[update.message.chat_id] = {} 
    update.message.reply_text('What is your poll question?')
    return 1

def pollquestion(bot,update):
    global pobj
    pobj[update.message.chat_id]["question"] = update.message.text
    update.message.reply_text('Enter the options in new lines : ')
    return 2

def polloptions(bot,update):
    global pobj
    chat_id = update.message.chat_id
    options = update.message.text.split("\n")
    options_str = "\n".join([str(1+options.index(op)) + ") " + op for op in options])

    update.message.reply_text('Call for Vote : \n'+
    pobj[update.message.chat_id]["question"] + '\n' + options_str + 
    '\nVote by using:\n  pls vote 2\nShow votes:\n  pls vote\nEnd vote and show results:\n  pls vote end')
    create_poll(chat_id, pobj[chat_id]["question"], options)

    return ConversationHandler.END


def pollcancel(bot,update):
    chat_id = update.message.chat_id
    end_poll(chat_id)
    update.message.reply_text('Poll cancelled.')
    return ConversationHandler.END

poll_handler = ConversationHandler(
    entry_points = [RegexHandler("^(?i)(pls poll)$", pollbegin)],

    states = {
        1 : [MessageHandler(Filters.text, pollquestion)],
        2 : [MessageHandler(Filters.text,polloptions)]
    },

    fallbacks = [RegexHandler("^(pls end|pls cancel)$", pollcancel)]

)

def poll_extras_handler(bot,update,msg_list):
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    if msg_list[1] == "vote":
        

        # view poll
        if len(msg_list) == 2:
            view_poll(bot,update)
        
        # vote end or vote <n>
        elif len(msg_list) > 2 and msg_list[2]=="end":
            view_poll(bot, update)
            end_poll(chat_id)
            update.message.reply_text("Poll has been ended.")
        
        # add vote
        else:
            n = int(msg_list[2]) -1
            options = get_poll_options(chat_id)
            if n in range(0,len(options)): 
                vote_poll(chat_id, username, 1+n)
                update.message.reply_text("Voted!")
            else:
                update.message.reply_text("Option out of range!")


def view_poll(bot,update):
    votes = get_votes(update.message.chat_id)
    votes_str = "Votes :\n"
    for option in votes:
        index, option, users = option
        votes_str += str(index) + ") "  + option
        if len(users) > 0:
            votes_str += " ("+ ", ".join(users) +")"
        votes_str += "\n"
    update.message.reply_text(votes_str)

    