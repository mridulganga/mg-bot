from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.db import add_todo, get_todos, clear_todos, remove_todo


def todo_handler(bot, update, msg_list):
    chat_id = update.message.chat_id

    if len(msg_list) == 1:
        todos = get_todos(chat_id)
        if todos.count == 0:
            update.message.reply_text("Todo list is empty.")
            return
        todo_str = "Todos :\n"
        for todo in todos:
            todo_str += "- " + todo["todo"] + "\n"
        update.message.reply_text(todo_str)

    elif msg_list[1] in ["remove", "delete"]:
        if len(msg_list) > 2:
            n = int(msg_list[2])
            remove_todo(chat_id, n)
        else:
            clear_todos(chat_id)
        update.message.reply_text("TODO(s) have been removed.")

    elif msg_list[1] in ["clear","removeall"]:
        clear_todos(chat_id)
        update.message.reply_text("TODO(s) have been removed.")
    
    else:
        add_todo(chat_id, " ".join(msg_list[1:]))
        update.message.reply_text("TODO has been added.")
