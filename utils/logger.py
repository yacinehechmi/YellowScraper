import logging


def setup_logger(logger_name, logfile):
    logger = logging.getLogger(logger_name)
    file_handler = logging.FileHandler(logfile)
    cstream_handler = logging.StreamHandler()
    logger.setLevel(logging.ERROR)
    file_handler.setLevel(logging.ERROR)
    cstream_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("""%(asctime)s - %(name)s -
                                  %(levelname)s - %(message)s""")
    file_handler.setFormatter(formatter)
    cstream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(cstream_handler)
    return logger
