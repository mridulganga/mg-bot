import logging

logging.config.fileConfig('logging.conf')
debug_logger = logging.getLogger('dlog')
msg_logger = logging.getLogger('mlog')


if __name__=="__main__":
    r = logging.getLogger()
    while(True):
        text = input()
        msg_logger.info(text)