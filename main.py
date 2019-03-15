from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# from app.logger import debug_logger

# need this to log erros
import logging
import sys
sys.stderr = open("logs/stderr","a")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',	
                    level=logging.INFO)	
logger = logging.getLogger(__name__)
# do not remove


import app.basic as basic
from app.poll import poll_handler

updater = None


def main():
    global updater
    f = open('api/token','r')
    token = f.read()
    updater = Updater(token)
    f.close()

    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", basic.start))
    dp.add_handler(CommandHandler("help", basic.help))

    dp.add_handler(poll_handler)
    dp.add_handler(MessageHandler(Filters.text, basic.msg_parser))


    dp.add_error_handler(basic.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()