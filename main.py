import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# from app.basic import start, help, error, msg_parser
import app.basic as basic

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = None


def main():
    global updater
    updater = Updater("713920275:AAGzidB_hHqdm5XoaiUXQCK8RUg0HLDIjaI")

    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", basic.start))
    dp.add_handler(CommandHandler("help", basic.help))

    dp.add_handler(MessageHandler(Filters.text, basic.msg_parser))

    dp.add_error_handler(basic.error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()