import logging


import logging
import logging.config

# Say i have saved my configuration under ./myconf.conf
logging.config.fileConfig('logging.conf')
debug_logger = logging.getLogger('debug_logger')
msg_logger = logging.getLogger('msg_logger')

# logger.info('Test log')
# logger.warn('Warning')

# try:
#     1/0
# except:
#     logger.exception("Supporting exceptions too!")


# # create logger with 'spam_application'
# debug_logger = logging.getLogger('debug_logger')
# debug_logger.setLevel(logging.DEBUG)
# # create file handler which logs even debug messages
# # fh = logging.FileHandler('logs/debug.log')
# # fh.setLevel(logging.DEBUG)
# # create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# # create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# # fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# # add the handlers to the logger
# # debug_logger.addHandler(fh)
# debug_logger.addHandler(ch)



# msg_logger = logging.getLogger('msg_logger')
# msg_logger.setLevel(logging.INFO)
# # msg_fh = logging.FileHandler('logs/msg.log')
# # msg_fh.setLevel(logging.INFO)
# # msg_formatter = logging.Formatter('%(asctime)s - %(message)s')
# # msg_fh.setFormatter(msg_formatter)
# # msg_logger.addHandler(msg_fh)