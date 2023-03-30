import logging
from colorlog import ColoredFormatter
logging.getLogger("urllib3").setLevel(logging.ERROR)


class ConsoleLogger:
    def __init__(self, logger_name):
        logging.getLogger().handlers = []
        logging.basicConfig(level=logging.INFO)
        formatter = ColoredFormatter(
            '%(log_color)s%(process)d - %(threadName)s - %(asctime)s - %(levelname)s - %(message)s',
            log_colors={'DEBUG': 'white', 'INFO': 'cyan', 'WARNING': 'yellow',
                        'ERROR': 'red', 'CRITICAL': 'red,''bg_black'})
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.handlers[0].setFormatter(formatter)
        self.logger.propagate = False
