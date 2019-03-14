from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from app.logger import debug_logger


import app.basic as basic
from app.poll import poll_handler

updater = None


def main():
    global updater
    f1 = open('api/mg','r')
    f2 = open('api/gopika','r')
    mg_token = f1.read()
    gopika_token = f2.read()
    updater = Updater(gopika_token)

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