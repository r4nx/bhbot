import logging
from logging.handlers import RotatingFileHandler


def get_logger(logger_name, level=logging.INFO, file_name=None):
    logger = logging.getLogger(logger_name)

    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    if file_name is not None:
        file_handler = RotatingFileHandler(file_name, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(levelname)s - [%(asctime)s] %(filename)s[L:%(lineno)d] %(message)s'))
        logger.addHandler(file_handler)

    return logger
