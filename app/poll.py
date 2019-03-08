from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler


def save_poll():
    global poll
    f = open('data/poll','w')
    f.write(str(poll))
    f.close()

def load_poll():
    f = open('data/poll','r')
    data=f.read()
    f.close()
    return eval(data)

poll = load_poll()

poll_object = {
    "question" : "",
    "options" : [] ,
    "votes" : {}
}


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys


def pollbegin(bot, update):
    global poll
    pobj = dict(poll_object)
    poll[update.message.chat_id] = pobj
    save_poll()
    update.message.reply_text('What is your poll question?')
    return 1

def pollquestion(bot,update):
    global poll
    poll[update.message.chat_id]["question"] = update.message.text
    save_poll()
    update.message.reply_text('Enter the options in new lines : ')
    return 2

def polloptions(bot,update):
    global poll
    options = update.message.text.split("\n")
    poll[update.message.chat_id]["options"] = options
    save_poll()
    options_str = "\n".join([str(1+options.index(op)) + ") " + op for op in options])
    
    update.message.reply_text('Call for Vote: '+
    poll[update.message.chat_id]["question"] + '\n' + options_str + 
    '\nVote by using:\n  pls vote 2\nShow votes:\n  pls vote\nEnd vote and show results:\n  pls vote end'
    )
    return ConversationHandler.END

def pollcancel(bot,update):
    end_poll(bot,update)
    update.message.reply_text('Cancelled')
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
    global poll
    if msg_list[1] == "vote":
        # ensure dict for chat_id exists
        if not update.message.chat_id in poll:
            update.message.reply_text("Poll not created.\n  pls poll")
            return
        # view poll
        if len(msg_list) == 2:
            view_poll(bot,update)
            return
        # vote end or vote <n>
        if len(msg_list) > 2 and msg_list[2]=="end":
            end_poll(bot,update)
        else:
            pobj = poll[update.message.chat_id]
            print(pobj)
            n = int(msg_list[2]) -1
            if int(n) in range(len(pobj["options"])): 
                pobj["votes"][update.message.from_user.username] = n
                save_poll()
                update.message.reply_text("Voted!")
                print(str(update.message.chat_id) + pobj)
            else:
                update.message.reply_text("Option out of range!")


def view_poll(bot,update):
    global poll
    pobj = poll[update.message.chat_id]
    s = "Poll: " + pobj["question"] + "\nVotes: \n"
    for n in range(len(pobj["options"])):
        vs = getKeysByValue(pobj["votes"],n)
        s += str(n+1) + ") " + pobj["options"][n] + " = " + str(len(vs)) + "("+ ",".join(vs) +") \n"
    update.message.reply_text(s)


def end_poll(bot,update):
    global poll
    view_poll(bot,update)
    poll.pop(update.message.chat_id)
    save_poll()
    