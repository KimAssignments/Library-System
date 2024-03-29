
import os
import json
import time

from .Logging import get_logger, remove_handler
from .Path import Path


def valid_JSON(FILE_NAME):
    logger = get_logger('DB_Validation')

    FILE_PATH = Path().user_data_roaming_dir
    FILE = os.path.join(FILE_PATH, FILE_NAME)

    while True:
        try:
            if os.stat(FILE).st_size == 0:
                open(FILE, 'w', encoding = 'UTF-8').write('{}')

            with open(FILE, 'r', encoding = 'UTF-8') as f:
                json.load(f)

                logger = remove_handler(logger)
                return True

        except FileNotFoundError:
            open(FILE, 'w+', encoding = 'UTF-8')
            logger.debug("%s is created as it doesn't exist", FILE_NAME)

def pull_data(LOGGER_NAME, FILE_NAME):
    logger = get_logger(LOGGER_NAME)
    start_time = time.time() * 1000

    FILE_PATH = Path().user_data_roaming_dir
    FILE = os.path.join(FILE_PATH, FILE_NAME)

    valid_JSON(FILE_NAME)

    with open(FILE, 'r', encoding = 'UTF-8') as f:
        JSON = json.load(f)
        logger.debug('%s has been successfully loaded (Execution time: %.2f ms)', FILE_NAME, (time.time() * 1000 - start_time))

        logger = remove_handler(logger)
        return JSON

def push_data(LOGGER_NAME, FILE_NAME, DUMP_DATA):
    logger = get_logger(LOGGER_NAME)
    start_time = time.time() * 1000

    FILE_PATH = Path().user_data_roaming_dir
    FILE = os.path.join(FILE_PATH, FILE_NAME)

    valid_JSON(FILE_NAME)

    with open(FILE, 'w', encoding = 'UTF-8') as f:
        json.dump(DUMP_DATA, f, indent = 4, ensure_ascii = False, sort_keys = False)
        logger.debug('Data has been dumped successfully into %s (Execution time: %.2f ms)', FILE_NAME, (time.time() * 1000 - start_time))

        logger = remove_handler(logger)
        return True


class DB_Employee:

    @staticmethod
    def Retrieve():
        return pull_data('DB_Employee.Retrieve', 'DB_Employee.json')

    @staticmethod
    def Dump(Database):
        push_data('DB_Employee.Dump', 'DB_Employee.json', Database)

class DB_Member:

    @staticmethod
    def Retrieve():
        return pull_data('DB_Member.Retrieve', 'DB_Member.json')

    @staticmethod
    def Dump(Database):
        push_data('DB_Member.Dump', 'DB_Member.json', Database)

class DB_Storing:

    @staticmethod
    def Retrieve():
        return pull_data('DB_Storing.Retrieve', 'DB_Storing.json')

    @staticmethod
    def Dump(Database):
        push_data('DB_Storing.Dump', 'DB_Storing.json', Database)
