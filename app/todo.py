from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def save_todo(dic):
    f = open('data/todo','w')
    f.write(str(dic))
    f.close()

def load_todo():
    f = open('data/todo','r')
    data=f.read()
    f.close()
    return eval(data)


todo = load_todo()

def todo_handler(bot, update, msg_list):
    global todo

    # Make todo list for group
    if not update.message.chat_id in todo:
        todo[update.message.chat_id] = []


    if len(msg_list) == 1:
        if len(todo[update.message.chat_id]) > 0:
            todo_str = str("\n".join(["- " + s for s in todo[update.message.chat_id]]))
            update.message.reply_text(todo_str)
        else:
            update.message.reply_text("TODO list is empty.")
    elif msg_list[1] in ["remove", "delete"]:
        if len(msg_list) > 2:
            n = int(msg_list[2])
            todo[update.message.chat_id].pop(n-1)
            save_todo(todo)
        else:
            todo[update.message.chat_id].clear()
            save_todo(todo)
        update.message.reply_text("TODO has been removed.")
    elif msg_list[1] in ["clear","removeall"]:
        todo[update.message.chat_id].clear()
        save_todo(todo)
        update.message.reply_text("TODO has been cleared.")
    else:
        todo[update.message.chat_id].append(" ".join(msg_list[1:]))
        save_todo(todo)
        update.message.reply_text("TODO has been added.")