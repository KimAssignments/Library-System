
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from .Path import Path


FORMATTER = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s]	%(message)s')
CONSOLE_FORMATTER = logging.Formatter('%(message)s')
FILE_PATH = Path().user_data_roaming_dir
FILE_NAME = 'System.log'
LOG_FILE = os.path.join(FILE_PATH, FILE_NAME)

def _get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    return console_handler

def _get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount = 7)
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # Better to have too much log than not enough
    logger.addHandler(_get_console_handler())
    logger.addHandler(_get_file_handler())
    # With this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

def get_receipt_logger(EmployeeID):
    logger = logging.getLogger(EmployeeID)
    logger.setLevel(logging.DEBUG)

    file_handler = TimedRotatingFileHandler(os.path.join(FILE_PATH, 'Receipt.txt'),
                                            when='midnight')
    file_handler.setFormatter(
        logging.Formatter('[%(asctime)s][EmployeeID: %(name)s]\n%(message)s\n\n')
    )

    logger.addHandler(file_handler)
    logger.propagate = False
    return logger

def remove_handler(logger):
    for h in range(len(logger.handlers)): logger.removeHandler(logger.handlers[0])
    return logger

def shutdown():
    logging.shutdown()
    return True
