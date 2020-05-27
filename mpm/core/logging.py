import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import coloredlogs
from mpm.core.__init__ import LOGGING_DIR
FORMATTER_FULL = logging.Formatter(
    "[%(levelname)s](%(asctime)s)LINE: %(lineno)d %(pathname)s - %(name)s %(funcName)s - %(message)s")
FORMATTER = logging.Formatter(
    "[%(levelname)s](%(asctime)s) %(name)s %(funcName)s - %(message)s")

def get_logging():
    SUCCESS_LEVEL = 25
    logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
    def success(self, message, *args, **kws):
        if self.isEnabledFor(SUCCESS_LEVEL):
            # Yes, logger takes its '*args' as 'args'.
            self._log(SUCCESS_LEVEL, message, args, **kws)
    logging.Logger.success = success
    return logging


def get_console_handler(level=logging.INFO):
    logging = get_logging()
    console_handler = logging.StreamHandler()#sys.stdout)


    formatter = coloredlogs.ColoredFormatter(
        "[%(levelname)s](%(asctime)s) %(name)s %(funcName)s - %(message)s",
        # log_colors={
        #     'DEBUG': 'cyan',
        #     'INFO': 'blue',
        #     'WARNING': 'yellow',
        #     'ERROR': 'red',
        #     # 'SUCCESS': 'green',
        #     'CRITICAL': 'red'
        # }
    )
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    return console_handler


def get_file_handler(file_name, level=logging.DEBUG, formatter=None):
    file_handler = TimedRotatingFileHandler(
        LOGGING_DIR / file_name, when='midnight')
    file_handler.setLevel(level)
    if formatter:
        file_handler.setFormatter(formatter)
    return file_handler


def getLogger(logger_name):
    if not LOGGING_DIR.is_dir():
        LOGGING_DIR.mkdir()
    logging = get_logging()
    logging.basicConfig(level=logging.DEBUG)
    
    logger = logging.getLogger(logger_name)

    logger.addHandler(get_console_handler(level=logging.INFO))
    logger.addHandler(get_file_handler(
        "debug.log", logging.DEBUG, formatter=FORMATTER_FULL))
    logger.addHandler(get_file_handler(
        "error.log", logging.ERROR, formatter=FORMATTER_FULL))
    logger.propagate = False
    return logger
