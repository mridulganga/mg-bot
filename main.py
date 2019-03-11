import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# from app.basic import start, help, error, msg_parser
import app.basic as basic
from app.poll import poll_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = None


def main():
    global updater
    mg_token = "713920275:AAGzidB_hHqdm5XoaiUXQCK8RUg0HLDIjaI"
    gopika_token = "715910035:AAFNGBByrhz-uiBfcOHVd84JsQSg3HHntOM"
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