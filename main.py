import os
import sys

import sentry_sdk
sentry_sdk.init(os.environ["SENTRY"])

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


import app.basic as basic
from app.poll import poll_handler

updater = None


def main():
    global updater

    token = os.environ["TELEGRAM"]
    updater = Updater(token)

    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", basic.start))
    dp.add_handler(CommandHandler("help", basic.help_handler))

    dp.add_handler(poll_handler)
    dp.add_handler(MessageHandler(Filters.text, basic.msg_parser))


    dp.add_error_handler(basic.error)

    if len(sys.argv) > 1:
        if sys.argv[1] == "local":
            updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                        port=int(os.environ["PORT"]),
                        url_path=token)
        updater.bot.set_webhook("https://telegram-mg-bot.herokuapp.com/" + token)


    updater.idle()


if __name__ == '__main__':
    main()