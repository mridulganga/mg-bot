from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# need this to log erros
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',	
                    level=logging.INFO)	
logger = logging.getLogger(__name__)
# do not remove


import app.basic as basic
from app.poll import poll_handler

updater = None


def main():
    global updater

    token = os.environ["TELEGRAM"]
    updater = Updater(token)

    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", basic.start))
    dp.add_handler(CommandHandler("help", basic.help))

    dp.add_handler(poll_handler)
    dp.add_handler(MessageHandler(Filters.text, basic.msg_parser))


    dp.add_error_handler(basic.error)

    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                      port=os.environ["PORT"],
                      url_path=token)
    updater.bot.set_webhook("https://telegram-mg-bot.herokuapp.com/" + token)


    updater.idle()


if __name__ == '__main__':
    main()