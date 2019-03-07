from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

todo = {}

def todo_handler(bot, update, msg_list):
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
        else:
            todo[update.message.chat_id].clear()
        update.message.reply_text("TODO has been removed.")
    elif msg_list[1] in ["clear","removeall"]:
        todo[update.message.chat_id].clear()
        update.message.reply_text("TODO has been cleared.")
    else:
        todo[update.message.chat_id].append(" ".join(msg_list[1:]))
        update.message.reply_text("TODO has been added.")