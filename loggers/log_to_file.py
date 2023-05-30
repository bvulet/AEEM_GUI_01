# ------------------------------
# File name log_to_file.py
# ------------------------------


import logging
from logging.handlers import TimedRotatingFileHandler


def file_log(module_name, filename, days, interval, backupcount, encoding):

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    file_handler = TimedRotatingFileHandler(filename=filename, when=days, interval=interval,
                                            backupCount=backupcount, encoding=encoding, delay=False)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # file_handler = logging.FileHandler('/Users/Boris/Desktop/solidtorevit/application.log')
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    return logger
